import json


import requests


# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect


def indexlogin(request):
    return render(request, 'home.html')


def login1(request):
    request.method == "POST"
    username = request.POST.get("u")
    passwd = request.POST.get("p")
    code = get_token(username, passwd)

    if code.status_code == 201:
        # resp = code.headers.get("X-Subject-Token")
        # account = get_token_counters(resp)
        # resp1 = account.json()
        return redirect('/lx220/test')
    else:
        error_msg ="用户名或密码不正确，请重新登录"
        return render(request,"home.html",{
            'login_error_msg':error_msg,
        })


#
def token():

    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": 'admin',
                        "password": '1234'
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": 'admin'
                }
            }
        }
    }
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp
    return headers


#获取token login
def get_token(username, password):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": username,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": username
                }
            }
        }
    }
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    code = requests.post(url, data=json.dumps(data))
    print(code)
    return code


def get_token_counters(domain_token):
    url2 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27?format=json"
    headers = {}
    headers["X-Auth-Token"] = domain_token
    resp1 = requests.get(url2, headers=headers)
    return resp1

def indexmain(request):
    return render(request, 'main.html')


#添加容器
def indexmain1(request, data1):
    request.method == "POST"
    username = request.POST.get("u")
    passwd = request.POST.get("p")
    print(username)
    print(passwd)
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": "admin",
                        "password": "1234"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }
    # 添加容器
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp

    url3 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/"+str(data1)+""
    requests.put(url3, headers=headers)

    return redirect("/lx220/test/")


#进入容器
def indexmain2(request, data2):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": "admin",
                        "password": "1234"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }
    # 进入容器
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp
    # print(data2)
    url4 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/" + str(data2)+"?format=json"
    resp3 = requests.get(url4, headers=headers)
    # print(resp3.text)
    resp4 = resp3.json()
    # print(resp4)
    pages = Paginator(resp4, 3)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1

    page = pages.get_page(page_number)

    return render(request, 'main2.html', {'resp1': page, 'data2': data2})


#查看对象内容
def indexmain3(request, container, object, objectname, content_type):
    token = request.session.get("token", None)
    headers = {}
    headers["X-Auth-Token"] = token
    url = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/" + str(container) + "/" + str(object) + "?format=json"
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    import base64
    resp_str = str(base64.b64encode(resp.content), 'utf-8')
    if objectname.startswith('image'):
        return render(request, 'main3.html', {'resp_img': resp_str, 'container': container, 'object': object})
    elif objectname.startswith('video'):
        return render(request, 'main3.html', {'resp_video': resp_str, 'container': container, 'object': object})
    elif objectname.startswith('audio'):
        return render(request, 'main3.html', {'resp_audio': resp_str, 'container': container, 'object': object})
    else:
        return render(request, 'main3.html', {'resp_text': resp.text, 'container': container, 'object': object})

#删除对象
def indexmain4(request, data5, data6):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": "admin",
                        "password": "1234"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }
    # 删除对象
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp
    url5 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/"+data5+"/"+data6+"?format=json"
    requests.delete(url5, headers=headers)
    return redirect('/lx220/main2/'+data5)


#删除容器
def indexmain5(request, data7):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": "admin",
                        "password": "1234"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }
    # 删除容器
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp
    url6 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/" + data7 + "?format=json"
    resp1 = requests.get(url6, headers=headers)
    resp2 = resp1.json()
    for i in resp2:
        if i['name']:
            url7 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/" + data7 + "/" + i['name'] +"?format=json"
            requests.delete(url7, headers=headers)
            #print(i['name'])
    requests.delete(url6, headers=headers)
    return redirect('/lx220/test')


def render_to_response(param, param1):
    pass


#容器主页面
def test(request):
    headers = token()
    url2 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27?format=json"

    resp1 = requests.get(url2, headers=headers)
    resp2 = resp1.json()
    # print(resp1.text)
    pages = Paginator(resp2, 4)
    try:
        page_number = request.GET['page']
    except:
        page_number = 1

    page = pages.get_page(page_number)
    return render(request, 'main.html', {'resp1': page})


#上传文件
def uploadindex(request, data8):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": "admin",
                        "password": "1234"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }
    # 上传文件
    file_obj = request.FILES.get('myfile')
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    url2 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/"+data8+"/"+str(file_obj)
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp
    file_content = file_obj.read()
    # print('内容', file_content)

    # # name = file_obj.name
    # # print(name)
    # obj = open(str(file_obj),'r')
    # files = {'file': obj}
    requests.put(url2,  headers=headers, data=file_content,)
    return redirect('/lx220/main2/'+data8)


#下载文件
def downloadindex(request, data9, data10):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": "admin",
                        "password": "1234"
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }
    # 下载文件
    url = "http://192.168.10.177:5000/v3/auth/tokens"
    url2 = "http://192.168.10.177:8080/v1/AUTH_fb9366ba3e5f4acf920c728e87cdeb27/" + data9 + "/" + data10+"?format=json"
    resp = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    headers = {}
    headers["X-Auth-Token"] = resp
    datas=requests.get(url2, headers=headers)
    # datas.encoding = 'utf-8'
    response =StreamingHttpResponse(datas)
    response['content_type'] = "application/text"
    response['Content-Disposition'] = 'attachment;filename='+data10.encode('utf-8').decode('ISO-8859-1')#中文文件名才能正常下载
    # return redirect('/lx220/main2/'+data9)
    return response

class Httpresponse(object):
    pass