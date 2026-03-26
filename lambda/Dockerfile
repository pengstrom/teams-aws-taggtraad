FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

COPY index.py config.py error.py ${LAMBDA_TASK_ROOT}/
COPY adaptive_card/ ${LAMBDA_TASK_ROOT}/adaptive_card/
COPY business/ ${LAMBDA_TASK_ROOT}/business/
COPY teams/ ${LAMBDA_TASK_ROOT}/teams/
COPY aws/ ${LAMBDA_TASK_ROOT}/aws/

CMD ["index.handler"]
