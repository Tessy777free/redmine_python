import datetime
from redminelib import Redmine
from redminelib.exceptions import ResourceNotFoundError
import xml.etree.ElementTree as ET
import json
#import pandas as pd

""" Redmineを扱うモジュール """

api_key = "325385dca5c8737d5abbb16cde6fab9053600a5a"    # apiアクセスキー
redmine_url = "http://192.168.100.101:8081/"            # URL
redmine = Redmine(redmine_url, key=api_key)

json_dict = {}

class RedmineTool:
    """ Redmineを扱うクラス """
    def __init__(self):                  # コンストラクタ
        """ コンストラクタ """
        print ("init")

    def hello(self):
        print ("Hello, Python")

    def readAllTicketToXml(self):
        """ チケットを読み出しXMLへ保存する """
        try:
#            issues = redmine.issue.filter(assigned_to_id='me')
#            issues = redmine.issue.filter(updated_on='><2020-05-12|2020-05-15')  #"><"  => :label_between,
            # 直近7日間の更新チケットを取り出す
#            issues = redmine.issue.filter(updated_on='>t-7')  # ">t-" => :label_less_than_ago,
            # 直近7日間の更新チケットを取り出す
            issues = redmine.issue.filter(
                            groups_id='6',      # homeグループに割り当てられた
                            updated_on='>t-5')  # ">t-" => :label_less_than_ago,
            for issue in issues:
                print ('%d:%s' % (issue.id, issue.subject))
                # issue.export('pdf', savepath='./')    チケットをPDF出力

            json_dict = issues.json()
             # CSV出力
            df = pd.io.json.json_normalize(data = json_dict["issues"])
            df.to_csv(path_or_buf = "redmine.csv",index=None)

        except (ResourceNotFoundError):
            print ('Not found')

    def readXml(self):
        #xmlデータを読み込みます
        tree = ET.parse('issues.xml')
        #一番上の階層の要素を取り出します
        root = tree.getroot()

        for child in root:
            print(child.tag)
            print("issue id=" + child.find("id").text)
            print("project id=" + child.find("project").attrib["id"])
            print("tracker id=" + child.find("tracker").attrib["id"])
            print("status id=" + child.find("status").attrib["id"])
            print("priority id=" + child.find("priority").attrib["id"])
            print("author id=" + child.find("author").attrib["id"])
            print("assigned_to id=" + child.find("assigned_to").attrib["id"])
            print("subject=" + child.find("subject").text)
            if (child.find("description").text):    # 理由は分からないがタグのみの場合はこれで判定できる
                print("description=" + child.find("description").text)

            print("start_date=" + child.find("start_date").text)
            print("due_date=" + child.find("due_date").text)
            print("done_ratio=" + child.find("done_ratio").text)
            print("is_private=" + child.find("is_private").text)
            print("estimated_hours=" + child.find("estimated_hours").text)
            print("created_on=" + child.find("created_on").text)
            print("updated_on=" + child.find("updated_on").text)

            if (child.find("closed_on").text):    # 理由は分からないがタグのみの場合はこれで判定できる
                print("closed_on=" + child.find("closed_on").text)

            redmine.issue.update(
                child.find("id").text,
                project_id=child.find("project").attrib["id"],
                subject=child.find("subject").text,
                tracker_id=child.find("tracker").attrib["id"],
                #description='foo',
                #notes='A journal note',
                private_notes=child.find("is_private").text,
                status_id=child.find("status").attrib["id"],
                priority_id=child.find("priority").attrib["id"],
                assigned_to_id=child.find("author").attrib["id"],
                #parent_issue_id=345,
                #start_date=datetime.date(2014, 1, 1),
                #due_date=datetime.date(2014, 2, 1),
                estimated_hours=child.find("estimated_hours").text,
                done_ratio=child.find("done_ratio").text
                #custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
            )

r = RedmineTool()
#r.readAllTicketToXml()
r.readXml()