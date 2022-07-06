# # background: #FFA17F;  /* fallback for old browsers */
# # background: -webkit-linear-gradient(to top, #00223E, #FFA17F);  /* Chrome 10-25, Safari 5.1-6 */
# # background: linear-gradient(to top, #00223E, #FFA17F); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */


# # for signup
# # background: #77A1D3;  /* fallback for old browsers */
# # background: -webkit-linear-gradient(to bottom, #E684AE, #79CBCA, #77A1D3);  /* Chrome 10-25, Safari 5.1-6 */
# # background: linear-gradient(to bottom, #E684AE, #79CBCA, #77A1D3); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
# #  for home 
#  background: #C9FFBF;  /* fallback for old browsers */
# background: -webkit-linear-gradient(to left, #FFAFBD, #C9FFBF);  /* Chrome 10-25, Safari 5.1-6 */
# background: linear-gradient(to left, #FFAFBD, #C9FFBF); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
# # /////////////
# # background-image: linear-gradient(to top, #d9afd9 0%, #97d9e1 100%);
# # background-image: linear-gradient(to top, #fbc2eb 0%, #a6c1ee 100%);

# from celery import task
# from celery.utils.log import get_task_loggerfrom 
# from .contact_mail import send_mail_to

# # sleeplogger = get_task_logger(__name__)
# @task(name='contact_email_task')
# def contact_email_task(subject,message):
#   # logger.info('Sent Details')
#   return contact_email(subject,message)

# # def my_first_task(duration):
# #     subject= 'Celery'
# #     message= 'My task done successfully'
# #     receiver= 'receiver_mail@gmail.com'
# #     is_task_completed= False
# #     error=''
# #     try:
# #         sleep(duration)
# #         is_task_completed= True
# #     except Exception as err:
# #         error= str(err)
# #         logger.error(error)
# #     if is_task_completed:
# #         send_mail_to(subject,message,receivers)
# #     else:
# #         send_mail_to(subject,error,receivers)
# #     return('first_task_done')