FROM bankingfraud
WORKDIR /ManageModelService
ADD /ManageModelService /ManageModelService
EXPOSE 5195
CMD ["gunicorn", "-b", "0.0.0.0:5195", "main:app"]