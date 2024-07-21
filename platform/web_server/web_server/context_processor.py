from web_server import settings

def amplitude_settings(request):
    return {
        #'AMPLITUDE_API_KEY': settings.AMPLITUDE_API_KEY,
        'AMPLITUDE_API_KEY': 'NONE',
    }

#def blockchain_account(request):
#    blockchain_account = None
#    if request.user.is_authenticated:
#        blockchain_account = request.user.profile.wallet.owned_eth_account
#    return {
#        'BLOCKCHAIN_ACCOUNT': blockchain_account,
#    }

def runtime_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'PRODUCTION': settings.PRODUCTION,
    }
