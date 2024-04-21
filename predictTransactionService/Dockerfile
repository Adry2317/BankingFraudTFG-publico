FROM bankingfraud
WORKDIR /predictTransactionService
ADD /predictTransactionService /predictTransactionService
EXPOSE 5194
CMD ["gunicorn", "-b", "0.0.0.0:5194", "main:app"]