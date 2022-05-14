# Zalando Discount Generator

A discount generator for zalando, automatically generating 10% off discounts by signing up for the newsletter. I added automatic discount fetch from email to automate the whole process.

If you want to you can easily use proxies by pasting them into the 'proxies.txt' file but if you don't it will still work completely fine.

## Config.json
    Region:
This is the region you want your discounts to be generated in, you would for example put fr for france or it for italy etc.
    Catchall:
This is the catchall/domain, you would for example put @yourcatchallname.
    Imap-server:
The server of your inbox, gmail uses imap.gmail.com but you can easily adjust this if your catchall goes to another email type.
    Imap-email:
The email your catchall goes to, you would for example put filipg545@gmail.com
    Imap-password:
The password to the email your catchall goes to.

Important to note is you have to have imap enabled and potentially "allow less secure apps."
