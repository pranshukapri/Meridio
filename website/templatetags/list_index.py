from django import template
register = template.Library()

@register.filter
def index(List,i):
	return List[int(i)]

@register.filter
def get_element(item,element):
	print(item["friend"])
	if element == 'username':
		return item["friend"].username
	elif element == 'photo':
		return item["friend"].profile.avatar.url
	elif element == 'bio':
		return item["friend"].profile.bio

@register.filter
def get_chatcode(item):
	#print('chat'+str(item["chat_id"]))
	return item["chat_id"]
