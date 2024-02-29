from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



username ='priyankagupta@ms.du.ac.in'
password = 'Priyanka@011'


# In[ ]:


driver = webdriver.Chrome()
driver.get('https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en-US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Aindv_identity&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3D092a214d300ac62ef7553cb9e1f65f3f&state=userLogin%7CtxId%3DA7320C2C7F38D138ED975DBFAB4BFA25.i-037e98c7be7ddc14a%3A5&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS')
time.sleep(10)




driver.find_element_by_css_selector('#bdd-elsSecondaryBtn').click()
driver.find_element_by_id("bdd-email").send_keys(username)
driver.find_element_by_css_selector("#bdd-els-searchBtn").click()
driver.find_element_by_id("bdd-password").send_keys(password)
driver.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()


print("logged in")