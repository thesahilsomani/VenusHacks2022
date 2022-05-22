import requests

class Grammar:
    def __init__(self, file_name = 'grammarAPIKEY.txt'):
        try:
            with open(file_name) as f:
                self.api_key = f.readlines()[0].rstrip()
        except:
            print("Error with Opening API_KEY File")

    def check(self, input):
        errors = self._find_errors(input)
        fixed = self._fix_errors(input, errors)
        return fixed

    def _find_errors(self, input):
        text = '+'.join(input.split())
        url = f'https://api.textgears.com/grammar?key={self.api_key}&text={text}&language=en-GB'
        response = requests.post(url).json()
        return response

    def _fix_errors(self, input, response):
        fixed = input
        errors = response['response']['errors']
        if len(errors) == 0:
            return input+'\n'+'(No errors found)'
        for e in errors:
            bad = e['bad']
            better = e['better'][0]
            fixed = fixed.replace(bad, better)
        return fixed
