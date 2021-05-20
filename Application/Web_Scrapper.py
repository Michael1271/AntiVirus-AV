import smtplib
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup

# A Program that deals with web scrapping
__author__ = 'Michael Khoshahang'


def get_latest_windows_version():
    """
    The function gets the requested data from the give website - the latest version and os build.
    :return: list of the requested data from the website - the latest version and os build
    :rtype: tuple
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
    url = "https://winreleaseinfoprod.blob.core.windows.net/winreleaseinfoprod/en-US.html"
    html_page = requests.get(url, headers=headers)
    content = BeautifulSoup(html_page.content, 'html.parser')
    windows_version = content.find('h3').get_text()[8:10]
    table = content.body.find("table", attrs={"class": "cells-centered"})
    version_properties = table.find("tr")
    version_properties = [
        th.text for th in version_properties if 'th' in str(th)]
    latest_version = table.find("tr", attrs={"class": "highlight"})
    latest_version = latest_version.text.split("\n")[1:-2]
    dictionary = dict(zip(version_properties, latest_version))
    os_build = dictionary['OS build']

    return windows_version, os_build


def get_latest_software_version():
    """
    The function gets the latest version of the AntiVirus AV software and returns it.
    :return: the latest version of the AV software
    :rtype: str
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"}
    url = "https://antivirus-av-website.micha1245.repl.co/Downloads"
    html_page = requests.get(url, headers=headers)
    content = BeautifulSoup(html_page.content, 'html.parser')
    version = content.find("b")
    return version.text


def send_welcome_mail(receiver_mail, name, username, password):
    """
    the function sends an email to the user's mail using html and css templates.
    :param receiver_mail: the user's mail
    :param name: the name of the user
    :param username: the username of the user
    :param password: the password of the user
    :return: None
    """
    from Secret_Variables import EMAIL_ADDRESS
    from Secret_Variables import EMAIL_PASSWORD
    from Cryptography import decrypt

    msg = EmailMessage()
    msg['Subject'] = 'Welcome To AntiVirus AV Services'
    msg['from'] = EMAIL_ADDRESS
    msg['To'] = decrypt(receiver_mail)
    msg.add_alternative(
        f"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>Welcome To AntiVirusAV!</title>
    <!--[if (mso 16)]>
                                                        <style type="text/css">
    a (text-decoration: none;)
    </style>
                                                        <![endif]-->
    <!--[if gte mso 9]>
                                                        <style>sup ( font-size: 100% !important; )</style>
                                                        <![endif]-->
    <!--[if gte mso 9]>
                                                        <xml>
                                                                <o:OfficeDocumentSettings>
                                                                        <o:AllowPNG></o:AllowPNG>
                                                                        <o:PixelsPerInch>96</o:PixelsPerInch>
                                                                </o:OfficeDocumentSettings>
                                                        </xml>
                                                        <![endif]-->
    <!--[if gte mso 9]>
                                                        <style>sup ( font-size: 100% !important; )</style>
                                                        <![endif]-->
    <!--[if gte mso 9]><style>sup (font-size: 100% !important; )</style><![endif]-->
</head>

<body>
    <div class="es-wrapper-color">
        <!--[if gte mso 9]>
                                                                <v:background
                                                                        xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                                                                        <v:fill type="tile" color="#ffffff"></v:fill>
                                                                </v:background>
                                                                <![endif]-->
        <table class="es-wrapper" style="background-position: center top;" width="100%" cellspacing="0" cellpadding="0">
            <tbody>
                <tr>
                    <td class="esd-email-paddings" valign="top">
                        <table class="es-header esd-header-popover" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" esd-custom-block-id="15610" align="center" bgcolor="#f4f7fa" style="background-color: #f4f7fa;">
                                        <table class="es-header-body" style="background-color: #ffffff;" width="600" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/0ea899c7-902e-4340-8912-233cb5c11dc6/images/3531613495468236.png" alt style="display: block;" width="110"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" bgcolor="#f4f7fa" style="background-color: #f4f7fa;">
                                        <table class="es-content-body" style="background-color: #f4f7fa;" width="600" cellspacing="0" cellpadding="0" align="center" bgcolor="#F4F7FA">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table style="border-radius: 3px; border-collapse: separate; background-color: #fcfcfc;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#fcfcfc">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-m-txt-l es-p30t es-p20r es-p20l" align="left" bgcolor="#FCFCFC">
                                                                                        <h2 style="color: #333333;">Welcome!</h2>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p10t es-p20r es-p20l" bgcolor="#FCFCFC" align="left">
                                                                                        <p style="font-size: 16px; font-family: 'open sans', 'helvetica neue', helvetica, arial, sans-serif;">Hi {decrypt(name)}, we’re glad you’re here!<br>You have successfully signed up to your AntiVirus Service.<br><br>Now, You can run the AntiVirus software by logging in to your account.<br>If you would like to download the Software please <a href="https://antivirus-av-website.micha1245.repl.co/Downloads">Click Here</a>.<br>for your convenience your Account Information&nbsp;is attached to this Mail.</p>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="esd-structure es-p30t es-p20r es-p20l" style="background-color: #fcfcfc;" esd-custom-block-id="15791" bgcolor="#FCFCFC" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="560" valign="top" align="center">
                                                                        <table style="border-color: #efefef; border-style: solid; border-width: 1px; border-radius: 3px; border-collapse: separate; background-color: #ffffff;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p20t es-p15b" align="center">
                                                                                        <h3 style="color: #333333;">Your account information:</h3>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text" align="center" bgcolor="#FCFCFC">
                                                                                        <p style="font-size: 16px;">Username: {decrypt(username)}</p>
                                                                                        <p style="font-size: 16px;">Password: {decrypt(password)}&nbsp;</p>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-button es-p20t es-p20b es-p10r es-p10l" align="center" bgcolor="#FCFCFC"><span class="es-button-border" style="background: #1671fa;"></span></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" bgcolor="#f4f7fa" style="background-color: #f4f7fa;">
                                        <table bgcolor="#F4F7FA" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: #f4f7fa;">
                                            <tbody>
                                                <tr>
                                                    <td class="es-p20t es-p20r es-p20l esd-structure" align="left" bgcolor="#FCFCFC" style="background-color: #fcfcfc;">
                                                        <table cellpadding="0" cellspacing="0" width="100%">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="560" class="esd-container-frame" align="center" valign="top">
                                                                        <table cellpadding="0" cellspacing="0" width="100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-text" bgcolor="#FCFCFC">
                                                                                        <p style="font-size: 15px; font-family: 'open sans', 'helvetica neue', helvetica, arial, sans-serif;"><b>We're here for you! Contact us for any help!</b><br><br></p>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-social es-p5t es-p25b es-p20r es-p20l" align="center" style="font-size: 0px; background-color: #fcfcfc;" bgcolor="#FCFCFC">
                                                                                        <table class="es-table-not-adapt es-social" cellspacing="0" cellpadding="0">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href><img title="Facebook" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/facebook-logo-black.png" alt="Fb" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://viewstripo.email/"><img title="Twitter" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/twitter-logo-black.png" alt="Tw" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://viewstripo.email/"><img title="Instagram" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/instagram-logo-black.png" alt="Inst" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://viewstripo.email/"><img title="Youtube" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/youtube-logo-black.png" alt="Yt" width="32"></a></td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="esd-footer-popover es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" style="background-color: #f4f7fa;" bgcolor="#F4F7FA" align="center">
                                        <table class="es-content-body" style="background-color: #ffffff;" width="600" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure es-p30t es-p30b es-p20r es-p20l" align="left" bgcolor="#FCFCFC" style="background-color: #fcfcfc;">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="560" valign="top" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/0ea899c7-902e-4340-8912-233cb5c11dc6/images/311613495479945.png" alt style="display: block;" width="100"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>

</html>
        """, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def send_account_info(receiver_mail, username, password):
    """
    the function sends an email to the user's mail using html and css templates.
    :param receiver_mail: the user's mail
    :param username: the username of the user
    :param password: the password of the user
    :return: None
    """
    from Secret_Variables import EMAIL_ADDRESS
    from Secret_Variables import EMAIL_PASSWORD
    from Cryptography import decrypt

    msg = EmailMessage()
    msg['Subject'] = 'Welcome To AntiVirus AV Services'
    msg['from'] = EMAIL_ADDRESS
    msg['To'] = decrypt(receiver_mail)
    msg.add_alternative(
        f"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>Welcome To AntiVirus AV!</title>
    <!--[if (mso 16)]>
                            <style type="text/css">
    a (text-decoration: none;)
    </style>
                            <![endif]-->
    <!--[if gte mso 9]>
                            <style>sup ( font-size: 100% !important; )</style>
                            <![endif]-->
    <!--[if gte mso 9]>
                            <xml>
                                <o:OfficeDocumentSettings>
                                    <o:AllowPNG></o:AllowPNG>
                                    <o:PixelsPerInch>96</o:PixelsPerInch>
                                </o:OfficeDocumentSettings>
                            </xml>
                            <![endif]-->
    <!--[if gte mso 9]>
                            <style>sup ( font-size: 100% !important; )</style>
                            <![endif]-->
    <!--[if gte mso 9]><style>sup (font-size: 100% !important; )</style><![endif]-->
</head>

<body>
    <div class="es-wrapper-color">
        <!--[if gte mso 9]>
                                <v:background
                                    xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                                    <v:fill type="tile" color="#ffffff"></v:fill>
                                </v:background>
                                <![endif]-->
        <table class="es-wrapper" style="background-position: center top;" width="100%" cellspacing="0" cellpadding="0">
            <tbody>
                <tr>
                    <td class="esd-email-paddings" valign="top">
                        <table class="es-header esd-header-popover" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" esd-custom-block-id="15610" align="center" bgcolor="#f4f7fa" style="background-color: #f4f7fa;">
                                        <table class="es-header-body" style="background-color: #ffffff;" width="600" cellspacing="0" cellpadding="0" align="center" bgcolor="#ffffff">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/0ea899c7-902e-4340-8912-233cb5c11dc6/images/3531613495468236.png" alt style="display: block;" width="110"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" bgcolor="#f4f7fa" style="background-color: #f4f7fa;">
                                        <table class="es-content-body" style="background-color: #f4f7fa;" width="600" cellspacing="0" cellpadding="0" align="center" bgcolor="#F4F7FA">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table style="border-radius: 3px; border-collapse: separate; background-color: #fcfcfc;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#fcfcfc">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-m-txt-l es-p30t es-p20r es-p20l" align="left" bgcolor="#FCFCFC">
                                                                                        <h2 style="color: #333333;">Welcome!</h2>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p10t es-p20r es-p20l" bgcolor="#FCFCFC" align="left">

                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="esd-structure es-p30t es-p20r es-p20l" style="background-color: #fcfcfc;" esd-custom-block-id="15791" bgcolor="#FCFCFC" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="560" valign="top" align="center">
                                                                        <table style="border-color: #efefef; border-style: solid; border-width: 1px; border-radius: 3px; border-collapse: separate; background-color: #ffffff;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p20t es-p15b" align="center">
                                                                                        <h3 style="color: #333333;">Your account information:</h3>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text" align="center" bgcolor="#FCFCFC">
                                                                                        <p style="font-size: 16px;">Username: {decrypt(username)}</p>
                                                                                        <p style="font-size: 16px;">Password: {decrypt(password)}&nbsp;</p>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-button es-p20t es-p20b es-p10r es-p10l" align="center" bgcolor="#FCFCFC"><span class="es-button-border" style="background: #1671fa;"><a href="AntiVirus-AV-Project.michael1271.repl.co" class="es-button" target="_blank" style="font-family: &quot;open sans&quot;, &quot;helvetica neue&quot;, helvetica, arial, sans-serif; background: #1671fa; border-color: #1671fa;"></span></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table cellpadding="0" cellspacing="0" class="es-content" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" bgcolor="#f4f7fa" style="background-color: #f4f7fa;">
                                        <table bgcolor="#F4F7FA" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: #f4f7fa;">
                                            <tbody>
                                                <tr>
                                                    <td class="es-p20t es-p20r es-p20l esd-structure" align="left" bgcolor="#FCFCFC" style="background-color: #fcfcfc;">
                                                        <table cellpadding="0" cellspacing="0" width="100%">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="560" class="esd-container-frame" align="center" valign="top">
                                                                        <table cellpadding="0" cellspacing="0" width="100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-text" bgcolor="#FCFCFC">
                                                                                        <p style="font-size: 15px; font-family: 'open sans', 'helvetica neue', helvetica, arial, sans-serif;"><b>We're here for you! Contact us for any help!</b><br><br></p>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-social es-p5t es-p25b es-p20r es-p20l" align="center" style="font-size: 0px; background-color: #fcfcfc;" bgcolor="#FCFCFC">
                                                                                        <table class="es-table-not-adapt es-social" cellspacing="0" cellpadding="0">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href><img title="Facebook" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/facebook-logo-black.png" alt="Fb" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://viewstripo.email/"><img title="Twitter" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/twitter-logo-black.png" alt="Tw" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://viewstripo.email/"><img title="Instagram" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/instagram-logo-black.png" alt="Inst" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://viewstripo.email/"><img title="Youtube" src="https://tlr.stripocdn.email/content/assets/img/social-icons/logo-black/youtube-logo-black.png" alt="Yt" width="32"></a></td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="esd-footer-popover es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" style="background-color: #f4f7fa;" bgcolor="#F4F7FA" align="center">
                                        <table class="es-content-body" style="background-color: #ffffff;" width="600" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure es-p30t es-p30b es-p20r es-p20l" align="left" bgcolor="#FCFCFC" style="background-color: #fcfcfc;">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="560" valign="top" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/0ea899c7-902e-4340-8912-233cb5c11dc6/images/311613495479945.png" alt style="display: block;" width="100"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>

</html>
        """, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
