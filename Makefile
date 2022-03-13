.PHONY: view install clean

view: heatmap.html
	python -m webbrowser $<

heatmap.html: failed_attempts.txt
	pipenv run SSHHeatmap $< "$$IPINFO_TOKEN"

failed_attempts.txt:
	zgrep "authentication failure\| Failed password" /var/log/auth.log* > $@

install:
	pipenv install --deploy

clean:
	rm heatmap.html failed_attempts.txt
