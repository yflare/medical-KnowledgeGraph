from rdflib import ConjunctiveGraph, Literal, Namespace, URIRef
from rdflib_endpoint import SparqlEndpoint

# 创建一个 RDFLib 图形对象并加载数据
g = ConjunctiveGraph()
g.parse("combined(3).ttl", format="turtle")
