FROM bankingfraud
WORKDIR /singOutService
ADD /singOutService /singOutService
EXPOSE 5192
CMD ["gunicorn", "-b", "0.0.0.0:5192", "main:app"]