FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

COPY index.py config.py error.py ${LAMBDA_TASK_ROOT}/
COPY event/ ${LAMBDA_TASK_ROOT}/event/
COPY business/ ${LAMBDA_TASK_ROOT}/business/
COPY teams/ ${LAMBDA_TASK_ROOT}/teams/

CMD ["index.handler"]
