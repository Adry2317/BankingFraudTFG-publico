FROM bankingfraud
WORKDIR /singUpService
ADD /singUpService /singUpService
EXPOSE 5190
CMD ["gunicorn", "-b", "0.0.0.0:5190", "main:app"]