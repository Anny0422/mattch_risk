import re
import csv

csv_contents = csv.reader(open('news_connect_keywords.csv', 'r'))
#csv_risk = csv.reader(open('risk_label.csv', 'r'))
csv_risk = csv.reader(open('risk_example.csv', 'r'))


def get_json(csv_contents):
    contents = []
    for row in csv_contents:
        content = {}
        content['id'] = row[0]
        content['content'] = row[1].strip('\t\n')
        content['stoc_id'] = row[2]
        content['counts'] = row[3]
        contents.append(content)

    print('新闻数量：', len(contents))
    return contents

# def get_riskdict(csv_risk):
#     risk_dict = {}
#     for row in csv_risk:
#         risk_dict[row[0]] = row[1:]
#     #print(risk_dict)       #{'业绩风险': ['净利润,增长|增加', '交易细节未披露|未披露'], '违法违规': ['同比增长|同比下降', '交易细节未披露']}
#     print('风险类型数量为：', len(risk_dict), '风险类型为：', risk_dict.keys())    #风险类型数量为： 2 风险类型为： dict_keys(['业绩风险', '违法违规'])
#     return risk_dict

def get_riskdict(csv_risk):
    risk_dict = {}
    for row in csv_risk:
        risk_dict[row[0]] = row[1:]
    #print(risk_dict)       #{'业绩风险': ['净利润,增长|增加', '交易细节未披露|未披露'], '违法违规': ['同比增长|同比下降', '交易细节未披露']}
    print('风险类型数量为：', len(risk_dict), '风险类型为：', risk_dict.keys())    #风险类型数量为： 2 风险类型为： dict_keys(['业绩风险', '违法违规'])
    return risk_dict



def get_risklabel(contents, risk_dict):  #传入数据(目前为批量，后来要修改为单个)
    double_id = []
    texts = []
    #for i in range(len(contents)):
    for i in range(500):
        text = contents[i]   #取出第i篇新闻；是一个字典，存储的有id，content, stoc_id, counts
        stoc_id = text['stoc_id']
        content = text['content']
        counts = text['counts']
        #print(content)
        for key, value in risk_dict.items():   #遍历风险类型
            flag = True
            right_labels = str(value[0]).split(',')   #['净利润', '增长|增加']
            del_labels = str(value[1]).split(',')     #['交易细节未披露|未披露', '世纪天鸿']
            #print('保留的正则：', right_labels, '删除的正则：', del_labels)

            #并行的几个正则表达式，一旦有一个匹配不上，则不再往下进行
            for i in range(len(right_labels)):
                right_pattern = re.compile('%s' % (right_labels[i]))
                if not right_pattern.search(content):
                    flag = False
            if flag:
                #并行的几个删除的正则表达式，一旦有一个匹配不上，则继续往下进行
                for j in range(len(del_labels)):
                    del_pattern = re.compile('%s' % (del_labels[j]))
                    if not del_pattern.search(content):
                        flag = False
                if not flag:
                    for item in texts:  ##若此新闻之前已匹配上其他风险，则将risk添加一个元素
                        if item['id'] == text['id'] and text['id'] != None:
                            #print(key)
                            item['risk'].extend([key])
                            double_id.append(item['id'])
                            flag = True
                    if not flag:
                        jre = {}
                        jre['id'] = text['id']
                        jre['risk'] = [key]
                        jre['stoc_id'] = stoc_id
                        jre['content'] = content
                        jre['counts'] = counts
                        texts.append(jre)
                        #print(key)
    print(double_id)
    return texts


if __name__ == '__main__':
    contents = get_json(csv_contents)
    risk_dict = get_riskdict(csv_risk)
    texts = get_risklabel(contents, risk_dict)
    print(texts)

# def run():
#     insert = 'INSERT IGNORE INTO news_connect_risk(news_id, content, stock_id, risk, counts) VALUES (%s, %s, %s, %s, %s)'
#
#     db = Database()
#     db.connect('news_connect_risk')
#
#     for i in range(len(texts)):
#         data = texts[i]
#         db.execute(insert, [data['id'], data['content'], str(data['stock_id']), data['risk'], str(data['counts'])])
#
#     db.close()

# if __name__ == '__main__':
#      run()
