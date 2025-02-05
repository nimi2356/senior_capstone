import re
def html_filter(text):
    text_pass_time = re.sub(
        r'\[\[TIME\.START\]\]\s*(.*?)\s*\[\[TIME\.END\]\]',
        r'\n\1\n',
        text
    )

    text_pass_talk =  re.sub(r'\s*>>\s*', '\n', text_pass_time)


    cleaned_text = "\n".join(line.strip() for line in text_pass_talk.splitlines() if line.strip())
    return cleaned_text

if __name__ == '__main__':
    transcript = """
>> good morning. >> >> what are we supposed to think of this stuff? if the cfo of twitter is getting [[TIME.START]] 6:26 am [[TIME.END]] hacked that says something to me. >> i'm going to summarize what my boss wrote awhile ago. if you're going to work at twitter learn how to use twitter and a direct message. the cfo yesterday fell for something that pretty much anybody would fall for. people have fallen for clicking on a link and losing control. >> that's what he did. >> lost control of his account but this is the same guy that a few months ago was caught sending a direct message and sending it out to everybody. >> but if you're the cfo -- actually if you're anybody; i thought everyone had two factor authentication which is something where i have a password and they'll send me a code every time and they'll send it to my phone; that you're done. >> yes; that is a lot more secure. it's beyond me why twitter and facebook in particular given all the incidents haven't come to -- >> but they have it on twitter. you can do it on twitter. >> but doesn't -- he still [[TIME.START]] 6:27 am [[TIME.END]] clicked on a link. >> yeah. >> and even with two factor authentication. >> you click on the link. >> you still would have -- >> i think you can still lose control of your account in that case. it's one of those malware akounlts akounlta accounts that takes control of the local system. >> we're no closer to stopping any of the hack attacks than we were six months ago; a year -- whatever. it seems like we have no control whatsoever over this issue. forbes newsweek twitter; someone else today; someone else tomorrow. >> sony delta anthem. in the case of twitter and facebook those are low damage accounts. nothing really happened and nobody cared because there was nothing serious going on there but if you're sending sensitive messages -- >> here's what i'm trying to to figure out. the hackers that went after; for example; twitter; they weren't [[TIME.START]] 6:28 am [[TIME.END]] going specifically after him but he just made the mistake of clicking on the wrong thing. >> probably targeting million of people on twitter. >> newsweek different story. somebody decided they wanted that account. >> they wanted to get control of that account. >> when they hack that account they have to figure out the password. >> they do. some other means. usually malware. >> but that was a very specific attack. >> sony obviously a very specific attack. >> sony was a very specific attack. there was a zero day vulnerability involved. >> do you believe right now if a hacker was out there and they stieded decided they wanted to hack our accounts they could do it easy? it's that easy in. >> yeah. we're all potential victims [[TIME.START]] 6:29 am [[TIME.END]] here. there's things you can do. >> but apparently that may not be enough. >> you have to make it hard for them. i secured my e-mail accounts. >> how many passwords do you have? >> too many to count. >> too many to count. you have to find a way to manage them. use something -- >> do you believe in those things? do you believe in these dash lane? >> i'm terrified if they hack dash lane they have everything.
"""
    filtered_html = html_filter(transcript)
    print("Filtered HTML output:")
    print(filtered_html)