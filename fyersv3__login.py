import time
import pyotp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fyers_apiv3 import fyersModel
from selenium.webdriver.common.by import By

app_id = "XXXXXXXXXX-100"
secret_key = "XXXXXXXXXX"
redirect_uri = "http://www.trademyapi.com"
response_type = "code"  
state = "sample_state"

userName = 'dsjahdk'
totp='wikefghwdbcocadib'

pin1='1'
pin2='2'
pin3='3'
pin4='4'

# Create Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Optional: Run Chrome in headless mode

# Create a Chrome WebDriver instance with options
driver = webdriver.Chrome(options=chrome_options)

def generate_auth_code():

    session=fyersModel.SessionModel(
    client_id=app_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri, 
    response_type='code',
    grant_type='authorization_code')
    response = session.generate_authcode()
    
    driver = webdriver.Chrome()
    driver.get(response)
    time.sleep(20)
    driver.find_element(By.ID,"login_client_id").click()
    driver.find_element(By.ID,"fy_client_id").send_keys('XD11432')
    driver.find_element(By.ID,"clientIdSubmit").click()
    time.sleep(4)
    t=pyotp.TOTP(totp).now()
    print(t)
   

    driver.find_element(By.ID,"first").send_keys(t[0])
    driver.find_element(By.ID,"second").send_keys(t[1])
    driver.find_element(By.ID,"third").send_keys(t[2])
    driver.find_element(By.ID,"fourth").send_keys(t[3])
    driver.find_element(By.ID,"fifth").send_keys(t[4])
    driver.find_element(By.ID,"sixth").send_keys(t[5])
    driver.find_element(By.ID,"confirmOtpSubmit").click()
    time.sleep(3)


             
    driver.find_element(By.ID,"verify-pin-page").find_element(By.ID,"first").send_keys(pin1)
    driver.find_element(By.ID,"verify-pin-page").find_element(By.ID,"second").send_keys(pin2)
    driver.find_element(By.ID,"verify-pin-page").find_element(By.ID,"third").send_keys(pin3)
    driver.find_element(By.ID,"verify-pin-page").find_element(By.ID,"fourth").send_keys(pin4)

    driver.find_element(By.ID,"verifyPinSubmit").click()
    time.sleep(40)
    newurl = driver.current_url
    auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    driver.quit()
    return auth_code

auth_code = generate_auth_code()

session = fyersModel.SessionModel(
    client_id=app_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type="authorization_code"
)

# Set the authorization code in the session object
session.set_token(auth_code)

# Generate the access token using the authorization code
response2 = session.generate_token()

access_token = response2["access_token"]
a=open("access.txt",'w')
a.write(access_token)
a.close()
print("access_token=",access_token)

