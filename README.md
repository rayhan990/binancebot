1) Create a settings.py file in the settings folder

	The settings file requires this variables to be declared:

	INTERVAL = The interval used to monitor and execute trades, Default 10

	MIN_BALANCE = Min operable balance, binance should be 10$ but you can increase if required

	api_secret = Your binance api key

	api_key = your binance secret key

	error_log_email_sender = error email sender

	error_log_email_receiver = error email recipient

	smtp_server = the smtp server used to send the emails

	smtp_user = smtp username

	smtp_pass = smtp password



	example:

		INTERVAL = 10
		MIN_BALANCE = 10
		api_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		error_log_email_sender="test@gmail.com"
		error_log_email_receiver="test@gmail.com"
		smtp_server="smtp.provider.net"
		smtp_user="apikey"
		smtp_pass="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"