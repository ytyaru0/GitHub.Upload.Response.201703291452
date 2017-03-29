# GitHub.Upload.Add.CUI.Directory.201703281703
# `uploader.`を`cui.uploader.`にgrep置換する
#find . -type f| grep .py$ | xargs grep "uploader."
#find . -type f| grep .py$ | xargs sed -i 's/uploader./cui.uploader./g'

# GitHub.Upload.Response.201703291452
# `./web/http/Response.py`を`./web/service/github/api/v3/Response.py`に変更した。コードも修正したい。
find . -type f | grep '*.py$' | xargs grep "web.http.Response"
find . -type f | grep '*.py$' | xargs sed -i 's/web.http.Response/web.service.github.api.v3.Response/g'
# 関数呼出部分
# `self.response.Get(r, res_type='json')`を`self.response.Get(r)`に置換したい。
find . -type f | grep '*.py$' | xargs grep "self.response.Get("
find . -type f | grep '*.py$' | xargs sed -i "s/self.response.Get(r, res_type='json')/self.response.Get(r)/g"

