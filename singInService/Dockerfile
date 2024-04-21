FROM bankingfraud
WORKDIR /singInService
ADD /singInService /singInService
EXPOSE 5191
CMD ["gunicorn", "-b", "0.0.0.0:5191", "main:app"]