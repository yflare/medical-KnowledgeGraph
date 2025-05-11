from rdflib import ConjunctiveGraph, Namespace
from flask import Flask, request, render_template, redirect, url_for
import re

app = Flask(__name__) 

# 创建RDF图和命名空间
g=ConjunctiveGraph()
g.parse(r"combined.ttl", format="turtle")

#命名空间
ex=Namespace("http://example.com/")
medicine=Namespace("http://example.org/medicine/")
ann=Namespace("http://example.org/annotation/")
ql=Namespace("http://semweb.mmlab.be/ns/ql#")
rml=Namespace("http://semweb.mmlab.be/ns/rml#")
rr=Namespace("http://www.w3.org/ns/r2rml#")


# 解析用户查询并提取主语
def parse_query(query):
    # 定义查询模式和对应的提取规则
    patterns = {
        r"^(.+)的制作处方是什么": r"\1",  # 克应丸的制作处方是什么？
        r"^(.+)可以治疗什么病症": r"\1",  # 补血和气饮可以治疗什么病症？
        r"^(.+)的用量用法是什么": r"\1",  # 补血定痛汤的用量用法是什么？
        r"^(.+)不能服用哪些中药方剂": r"\1",  # 孕妇不能服用哪些中药方剂
        r"^如何制作(.+)": r"\1",  # 如何制作苍术难名丹?
        r"^服用(.+)的注意事项有哪些": r"\1",  # 服用仓耳散的注意事项有哪些？
        r"^在临床治疗(.+)时，可以使用哪些中药方剂": r"\1",  # 在临床治疗慢性鼻炎时，可以使用哪些中药方剂？
        r"^服用药品(.+)的注意事项是什么": r"\1",  # 服用药品盆炎净片的注意事项是什么？
        r"^药品(.+)可以治疗什么病症": r"\1",  # 药品益母草颗粒可以治疗什么病症？
        r"^若出现(.+)的病症，建议使用什么药品": r"\1",  # 若出现月经量少的病症，建议使用什么药品？
        r"^药品(.+)的用法用量是什么": r"\1"  # 药品诺金盆炎净片的用法用量是什么？
    }

    # 遍历模式，尝试匹配查询  
    for pattern, subject_pattern in patterns.items():  
        match = re.match(pattern, query)  
        #print(match)
        if match:  
            # 使用正则表达式提取主语  
            subject = match.group(1)  
            # 如果匹配的是“如何制作...”模式，则去除句末的问号  
            if pattern.startswith(r"^如何制作"):  
                subject = subject.rstrip('？')
            # 如果主语以“药品”开头，则去除这两个字  
            if subject.startswith('药品'):  
                subject = subject[2:]  # 移除前两个字符“药品”  
            return subject  # 返回提取的主语    
    else:  
        print("未匹配到查询模式")  



#克应丸的制作处方是什么？
def query_prescription(subject):
    medicine_name = subject  # 假设subject已经是正确的URI形式的字符串
    # 正确的命名空间定义
    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    # 构建SPARQL查询
    query = f"""
    {prefix}
    SELECT ?prescription
    WHERE {{
        <medicine:{medicine_name}> ex:hasPrescription ?prescription .
    }}
    """
    
    # 执行查询并返回结果
    results = g.query(query)
    
    # 初始化变量来存储处方信息
    prescriptions = []
    
    # 遍历结果集
    for result in results:
        # 提取处方信息
        prescription = result['prescription']
        prescriptions.append(str(prescription))

    # 检查是否找到处方信息
    if prescriptions:
        # 将处方信息列表转换为字符串，并返回
        return f"{subject}的制作处方是：'{' '.join(prescriptions)}'"
    

#补血和气饮可以治疗什么病症？
def query_function_indications(subject):
    
    medicine_name = subject

    # 构建SPARQL查询
    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    query = f"""
    {prefix}
    SELECT ?function_indications
    WHERE {{
        <medicine:{medicine_name}> ex:hasFunction ?function_indications .
    }}
    """
    # 执行查询并返回结果
    results = g.query(query)
    # 初始化变量来存储治疗病症
    functions = []
    
    # 遍历结果集
    for result in results:
        # 提取处方信息
        function_indications = result['function_indications']
        functions.append(str(function_indications))

    # 检查是否找到处方信息
    if functions:
        # 将处方信息列表转换为字符串，并返回
        return f"{subject}可以治疗的病症是：'{' '.join(functions)}'"
    
#补血定痛汤的用量用法是什么？
def query_usage_dosage(subject):
    medicine_name = subject

    # 构建SPARQL查询
    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    query = f"""
    {prefix}
    SELECT ?usage_dosage
    WHERE {{
        <medicine:{medicine_name}> ex:hasUsage ?usage_dosage .
    }}
    """
    # 执行查询
    results = g.query(query)
    
    # 初始化变量来存储用量用法信息
    usage_dosages = []
    
    # 遍历结果集
    for result in results:
        # 提取用量用法信息
        usage_dosage = result['usage_dosage']
        usage_dosages.append(str(usage_dosage))

    # 检查是否找到用量用法信息
    if usage_dosages:
        # 将用量用法信息列表转换为字符串，并返回
        return f"{subject}的用量用法是：'{' '.join(usage_dosages)}'"
    
#孕妇不能服用哪些中药方剂？
def query_medicines_by_note(subject):
    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    query_condition = subject

    # 构建SPARQL查询字符串
    query_str = f"""
    {prefix}
    SELECT DISTINCT ?medicine
    WHERE {{
        ?medicine a ex:Medicine .
        ?medicine ex:hasNote ?note .
        FILTER (contains(LCASE(STR(?note)), "{query_condition}"))
    }}
    """
    # 执行查询
    results = g.query(query_str)
    medicines = []

    # 遍历结果集
    for result in results:
        # 提取药物名称
        medicine_name = result['medicine']
        # 只添加药物名称，忽略URIRef对象
        medicines.append(str(medicine_name))

    # 检查是否找到药物名称
    if medicines:
        # 将药物名称列表转换为字符串，并返回
        return f"{subject}不能服用的中药方剂有：'{', '.join(medicines)}'"

#如何制作苍术难名丹？
def query_preparation_method(subject):
    medicine_name = subject

    # 构建SPARQL查询
    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    query = f"""
    {prefix}
    SELECT ?preparation_method
    WHERE {{
        <medicine:{medicine_name}> ex:hasPreparation ?preparation_method .
    }}
    """

    # 执行查询
    results = g.query(query)
    
    # 初始化变量来存储制作方法信息
    preparation_methods = []
    
    # 遍历结果集
    for result in results:
        # 提取制作方法信息
        preparation_method = result['preparation_method']
        preparation_methods.append(str(preparation_method))

    # 检查是否找到制作方法信息
    if preparation_methods:
        # 将制作方法信息列表转换为字符串，并返回
        return f"{subject}的制作方法是：'{' '.join(preparation_methods)}'"
    

#服用一厘金的注意事项有哪些？
def query_medicine_precautions(subject):
    medicine_name = subject

    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    query = f"""
    {prefix}
    SELECT ?note
    WHERE {{
        <medicine:{medicine_name}> ex:hasNote ?note .
    }}
    """
    results = g.query(query)
    # 初始化变量来存储制作方法信息
    notes = []
    
    # 遍历结果集
    for result in results:
        # 提取注意事项信息
        note = result['note']
        notes.append(str(note))

    # 检查是否找到注意事项信息
    if notes:
        # 将注意事项信息列表转换为字符串，并返回
        return f"{subject}的注意事项是：'{' '.join(notes)}'"
#在临床治疗慢性鼻炎时，可以使用哪些中药方剂？
#在临床治疗疥疮时，可以使用哪些中药方剂？
def query_clinical_applications(subject):
    clinical_condition = subject

    prefix = """
    PREFIX ex: <http://example.com/>
    PREFIX medicine: <http://example.org/medicine/>
    """
    query = f"""
    {prefix}
    SELECT ?medicine 
    WHERE {{
        ?medicine ex:hasClinicalApplication ?clinicalApplication .
        FILTER (contains(?clinicalApplication, "{clinical_condition}"))
    }}
    """
    results = g.query(query)
    # 初始化变量来存储药物名称
    clinical_applications = []

    # 遍历结果集
    for result in results:
        # 提取药物名称
        medicine_name = result['medicine']
        # 只添加药物名称，忽略URIRef对象
        clinical_applications.append(str(medicine_name))

    # 检查是否找到药物名称
    if clinical_applications:
        # 将药物名称列表转换为字符串，并返回
        return f"在临床治疗{subject}时，可以使用的中药方剂有：'{', '.join(clinical_applications)}'"


#服用药品盆炎净胶囊的注意事项有哪些？
#服用药品七制香附丸的注意事项有哪些？
#服用药品新生化颗粒的注意事项有哪些？
def query_drug_precautions(subject): 
    prefix = """  
    PREFIX ex: <http://example.com/>  
    """  
    # 使用REGEXP来匹配包含【注意事项】的文本段落  
    query_str = f"""  
    {prefix}  
    SELECT ?hasText  
    WHERE {{  
        ?drug ex:hasText ?hasText .  
        FILTER(CONTAINS(LCASE(?hasText), "{subject}"))  
        FILTER(CONTAINS(LCASE(?hasText), "注意事项"))  
    }}  
    """  
    # 假设g是已经设置好的RDF图对象，例如使用rdflib等库创建  
    results = g.query(query_str)  
      
    # 提取并返回注意事项文本  
    precautions = []  
    for result in results:  
        text = str(result[0])  
        start_index = text.find("【注意事项】")  
        if start_index != -1:  
            # 提取【注意事项】之后的内容，直到遇到下一个【或者文本结束  
            end_index = text.find("【", start_index + len("【注意事项】"))  
            precautions_text = text[start_index + 6:end_index] if end_index != -1 else text[start_index + 6:]  
            precautions.append(precautions_text.strip()) 
    if precautions:
        return f"{subject}的注意事项有:'{''.join(precautions[0])}'"  
#药品益母草颗粒可以治疗什么病症？
#药品盆炎净胶囊可以治疗什么病症？
def query_drug_indications(subject):
    prefix = """  
    PREFIX ex: <http://example.com/>  
    """  
    # 使用REGEXP来匹配包含【功能主治】的文本段落  
    query_str = f"""  
    {prefix}  
    SELECT ?hasText  
    WHERE {{  
        ?drug ex:hasText ?hasText . 
        FILTER(CONTAINS(LCASE(?hasText), "{subject}"))  
        FILTER(CONTAINS(LCASE(?hasText), "功能主治"))  
    }}  
    """  
    # 假设g是已经设置好的RDF图对象，例如使用rdflib等库创建  
    results = g.query(query_str)  
      
    # 提取并返回注意事项文本  
    indications = []  
    for result in results:  
        text = str(result[0])  
        start_index = text.find("【功能主治】")  
        if start_index != -1:  
            # 提取【功能主治】之后的内容，直到遇到下一个【或者文本结束  
            end_index = text.find("【", start_index + len("【功能主治】"))  
            indications_text = text[start_index + 6:end_index] if end_index != -1 else text[start_index + 6:]  
            indications.append(indications_text.strip())  
    if indications:
        return f"药品{subject}可以'{''.join(indications[0])}'" 

#药品金刚藤糖浆的用量用法是什么？
#药品康妇消炎栓的用量用法是什么？
def query_drug_usage_dosage(subject):
    prefix = """  
    PREFIX ex: <http://example.com/>  
    """  
    # 使用REGEXP来匹配包含【用法用量】的文本段落  
    query_str = f"""  
    {prefix}  
    SELECT ?hasText  
    WHERE {{  
        ?drug ex:hasText ?hasText . 
        FILTER(CONTAINS(LCASE(?hasText), "{subject}"))   
        FILTER(CONTAINS(LCASE(?hasText), "用法用量"))  
    }}  
    """  
    # 假设g是已经设置好的RDF图对象，例如使用rdflib等库创建  
    results = g.query(query_str)  
      
    # 提取并返回注意事项文本  
    usage_dosage = []  
    for result in results:  
        text = str(result[0])  
        start_index = text.find("【用法用量】")  
        if start_index != -1:  
            # 提取【用法用量】之后的内容，直到遇到下一个【或者文本结束  
            end_index = text.find("【", start_index + len("【用法用量】"))  
            usage_dosage_text = text[start_index + 6:end_index] if end_index != -1 else text[start_index + 6:]  
            usage_dosage.append(usage_dosage_text.strip())
    if usage_dosage:
        return f"{subject}的用量用法是:'{''.join(usage_dosage[0])}'"    

#若出现月经不调的病症，建议使用什么药品？
def query_drug_by_indication(subject):
    prefix = """  
    PREFIX ex: <http://example.com/>  
    """  
    # 使用REGEXP来匹配包含【功能主治】的文本段落  
    query_str = f"""  
    {prefix}  
    SELECT ?hasText  
    WHERE {{  
        ?drug ex:hasText ?hasText . 
        FILTER(CONTAINS(LCASE(?hasText), "{subject}"))  
    }}  
    """  
    # 假设g是已经设置好的RDF图对象，例如使用rdflib等库创建  
    results = g.query(query_str)  
      
    # 提取并返回注意事项文本  
    medicines = []  
    for result in results:  
        text = str(result[0])  
        start_index = text.find("【药品名称】")  
        if start_index != -1:  
            # 提取【商品名称】之后的内容，直到遇到下一个【或者文本结束  
            end_index = text.find("【", start_index + len("【药品名称】"))  
            medicines_text = text[start_index + 6:end_index] if end_index != -1 else text[start_index + 6:]  
            medicines.append(medicines_text.strip())  
    if medicines:
        return f"若出现{subject}的病症，建议使用药品'{''.join(medicines[0])}'"

@app.route('/')
def welcome():
    return render_template('welcome.html')

LARGE_MODEL_INTERFACE_URL = "https://yiyan.baidu.com/"
    
@app.route('/submit-query',  methods=['GET', 'POST'])
def submit_query():
    result = ""
    query = request.form.get('query', '')  
    #subject = parse_query(query)
    if request.method == 'POST' and query:
        subject = parse_query(query) 
        # 获取用户输入的查询
        if "制作处方是什么" in query:
            result=query_prescription(subject)
        #print(result)
        if "治疗什么病症" in query:
            if "药品" in query:
                result=query_drug_indications(subject)
           # print(result)
            else:
                result=query_function_indications(subject)
            #print(result)
        if "用量用法是什么" in query:
            if "药品" in query:
                result=query_drug_usage_dosage(subject)
                print(result)
            else:
                 result=query_usage_dosage(subject)
           # print(result)
        if "不能服用哪些中药方剂" in query:
            result=query_medicines_by_note(subject)
            #print(result)
        if "如何制作" in query:
            result=query_preparation_method(subject)
        # print(result)
        if "注意事项有哪些" in query:
            if "药品" in query:
                result=query_drug_precautions(subject)
            # print(result)
            else:
                result=query_medicine_precautions(subject)
                #print(result)
        if "临床治疗" in query:
            result=query_clinical_applications(subject)
            #print(result)
        if "建议使用什么药品" in query:
            result=query_drug_by_indication(subject)
            #print(result)
    # 如果result为空，即没有查询到结果或者不支持的查询形式
        if not result:
        # 可以在这里添加逻辑，显示一个消息告知用户将重定向到其他平台
            return redirect(LARGE_MODEL_INTERFACE_URL)
            #return render_template('web.html', result="很抱歉，我们暂时无法回答您的问题。请访问其他平台以获取帮助。\n文心一言:'https://yiyan.baidu.com/'", query=query)

    # 使用HTML模板显示结果
    #return render_template('welcome.html', result=result, query=query)
    return render_template('web.html', result=result, query=query)

if __name__ == '__main__':
    app.run(debug=True)