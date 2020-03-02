##实现支付宝demo ,所有实现接口的都放在sdk中
#固定格式，5个横杠
#公钥
alipay_public_key_string="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqTe9BH7cHNINmOSQCxzcI4HUgEeKLuBoI2tObZVM53+JsFm1RtAvV590pBCS8a1kCDiMFVJoJ1ut1N+YvTuLSi20u2+iAvCvnT8k8Mr4AT++GtSb5oKD8Tez/HHrw9yURc4ajtYgiJu+UWgXx1J8rVWLfDmqqUaURunO93IQ7lulTOpTghMtYedyxXXSPRzg3vt20aUqE2hxTxTiIvmpxeq38MGc1QgzfBEMNaALsN7JxuK7jC92npzxo60AvyNxEvivy8XyuFGIc77qBNgVOpOD6msIWoHkH8WFPPkGbjEhQIVhNJ8eWHoKXvAPGThQs9sTJLw84r34745CinLJwQIDAQAB
-----END PUBLIC KEY-----"""
#私钥
app_private_key_string="""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAqTe9BH7cHNINmOSQCxzcI4HUgEeKLuBoI2tObZVM53+JsFm1RtAvV590pBCS8a1kCDiMFVJoJ1ut1N+YvTuLSi20u2+iAvCvnT8k8Mr4AT++GtSb5oKD8Tez/HHrw9yURc4ajtYgiJu+UWgXx1J8rVWLfDmqqUaURunO93IQ7lulTOpTghMtYedyxXXSPRzg3vt20aUqE2hxTxTiIvmpxeq38MGc1QgzfBEMNaALsN7JxuK7jC92npzxo60AvyNxEvivy8XyuFGIc77qBNgVOpOD6msIWoHkH8WFPPkGbjEhQIVhNJ8eWHoKXvAPGThQs9sTJLw84r34745CinLJwQIDAQABAoIBAFcpQ642HfCmbaSMTnm64tVTQX7V2qJsqpdb5Wjil1tCwUxZ2NrhzxDmLHF5rAbaVgU6A0XUTZvASFi213jZW9TYmBhX1u6GxR5M8R0qnvYdvDEbxDXGkmnEVGw6zcL0MleGYv2h494Zwr0xzdW4ckniH1fcaECK/0NLmXSxh3EOYvCv8yuEIr4oAnCvYaMvE/nB5O9swx/h4FbxGJSR7DBRaglNEa6OhAiSFBgWLUtKD+Kqh8Kc2A4Oz6TQHwWiwIvPbfOCPos86fiPDbOphpgD/aAxeUIJjRk2rFOal6EclYynZt/hcCZ0sDc8FDs3ofdPuyx+m6NibQc2cJM8JoUCgYEA20RRo8vQH7tKK3qtpX5W5HYvVLqlqvPSRT1dXLfAAMDXVhmc++lItlwIxD4DECo3fzpTZslV85CoFjNDD3YqEMjUDVbSUFzTGFSPgrRzmgDIfgokNNN03R+/cCrd1Kf8q1VT4xEvk1KilG2PszPmyf9dmyyGtmp5xeJ4/jOfftMCgYEAxZD3PWxjPHhHxryueqPJFDFct5FoTEU3a7o4sFoqdum/VJBL0iI/+yQv9Bs9LQVMDxxbcNeYBbp+BEO5s1vvU5NBw9sEnwB07THbGDYmx3WvGlHyWVgWR0APv1Ap3fCM2aYlGNttTE6hYHtZtGENwAPLU24VM/HqJgKRklD7AJsCgYAEqfVamJE6u48eUaOz63YJsgHbuYSgmEMWufFscXQiD/gEmtLeAN5NErQVCISkKWG40RLJEutDHQaWQkzg3VCTvtHT3s7marMKx3GuBAyZb/7Tv395qC3KLkyyJBdH2LLlKhF4uPrcFVvj8FioJSh5j3b8P/w1kRo5/VE5hvuThQKBgQCTv1TWj58rEryCyIonVyNCQaQX99sq5ryKiMpqQBPvt+EJKZw6OrjkZOyjvlciuwplZoyPt/uNlSk2oTtYAdHaC48sHDe5fQr0c8tosN6RXdYkddIqtLB8elEMfrPAsWt0PUcS7s4vOcJ/t9+fANHanjvJWdLrdOfpoxQgewUrLwKBgQDKN7KuLAgtaBt7LCFKI5zykocTElQhbZuEjPcYsMkH0gy44J4IRb7rkmUbF7EVAUqUzS6GiVuEZxbyzLXgHcpAMrswuYTKq5X/FBlLcPKSV9GwKI7eCXGDEsCuQmHIfjUDyva+Ii/3ROdUQ5c3KRmCYf8KVsGKlR1fci+bd5XH4Q==
-----END RSA PRIVATE KEY-----"""

#1.导包 #在创建文件是不能使用alipay
from alipay import AliPay
#2.创建一个实例对象
alipay=AliPay(
    appid="2016101800717516",#商户的appid-在沙箱应用
    app_notify_url=None,
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",
    debug=False
)
#3.实例化一个订单
"""
subject, out_trade_no, total_amount,
                                  return_url=None, notify_url=None
"""
# order_string=alipay.api_alipay_trade_app_pay() #手机应用app支付
order_string=alipay.api_alipay_trade_page_pay(
          subject="平价超市", #交易主体
          out_trade_no="2009223427862893",#订单号
          total_amount="0.01",#交易金额 字符串 有的为了精确，单位为分
          return_url=None,#回调地址
          notify_url=None  #通知
)
#4.返回支付宝的支付url
result="https://openapi.alipaydev.com/gateway.do?"+order_string
print(result)