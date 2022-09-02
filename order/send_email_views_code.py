'''               
                
                user = request.user
                profile = UserProfile.objects.get(user_id=request.user.id)
                context = 
                {'shopcart': shopcart,
               'total': total,
               'profile': profile,
               'subtotal': subtotal,
               'user': user,
               'ordercode': ordercode,
               }

            # email = User.objects.get(userprofile=current_user.email)
            temp = render_to_string(
                'email.html', context)
            
            subject, from_email, to = 'EmailMultiAlternatives first', 'bpanther70@gmail.com', 'bpanther70@gmail.com'
            text_content = 'This is an important message.'
            html_content = temp
            msg = EmailMessage(subject, temp, from_email, [to])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()


            sub = 'send_mail option'
            message = '<h2>this is test message</h2>'
            host = 'bpanther70@gmail.com'
            recepient = 'bpanther70@gmail.com'

                
            send_mail(
                sub,
                temp,
                host,
                [recepient],
                fail_silently=False,
            )


            email = EmailMessage(
                'EmailMessage with temp',
                message,
                host,
                [recepient],
            )
            email.fail_silently=False
            email.send()

            
            subject, from_email, to = 'EmailMultiAlternatives last', 'bpanther70@gmail.com', 'bpanther70@gmail.com'
            text_content = 'This is an important message.'
            html_content = '<p>This is an <strong>important</strong> message.</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

'''