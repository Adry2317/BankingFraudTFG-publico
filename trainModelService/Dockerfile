FROM bankingfraud
WORKDIR /trainModelService
ADD /trainModelService /trainModelService
EXPOSE 5193
CMD ["gunicorn", "-b", "0.0.0.0:5193", "main:app"]