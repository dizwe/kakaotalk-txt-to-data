# kakaotalk-txt-to-data
txt로 내보낸 카카오톡 대화를 날짜,내용,url 데이터로 변환하는 프로그램입니다.

사용하실때 출처를 밝혀주세요.
문의는 dizwe2716@gmail.com이나 이슈로 남겨주세요.


Documents
-------------
>SPEC.

	 ● python3에서 작동합니다.

	 ● re,codecs,json 모듈을 사용했습니다.
	
>지원기능.
	
 	 ● 카카오톡 대화를 txt파일로 변환하면 이를 데이터로 변환합니다.
  
How to Use
-------------

시작하기
-------------
    import kakako_to_data # 모듈 import 
	
    data_object = File_to_data(str_fname) 
  
object를 return합니다.
	
str_fname : 카카오톡에서 저장된 txt파일 이름을 적어주세요.
  
*주의* : txt파일을 현재 디렉토리(ex.C://Python35)에 저장해주세요.  
  
Data list 얻기 
-------------
    data_list = data_object.get_dict_list()
		
return 형식 : dictionary들의 list

return list(data_lst) 내용 : 

    {'content_names': int 번호, 'content_dates': str 날짜, 'content_link': str list 링크 리스트, 'content_coms': str 본문}
		ex){'content_names': 317, 'content_dates': '2016-07-20 16:01', 'content_link': ['http://ppss.kr/archives/66089'], 'content_coms': '당장 느끼는 기분이 행복을 결정하지는 않습니다 | ㅍㅍㅅㅅ - http://ppss.kr/archives/66089'}
  
Data list 저장하기
-------------
    data_list.save_dict_list()
		
파일 이름을 python 창에 입력하면 현재 디렉토리에 json 파일이 저장됩니다.

저장된 json 파일은 dictionary 들의 list이고,

내용은

    {'content_names': int 번호, 'content_dates': str 날짜, 'content_link': str list 링크 리스트, 'content_coms': str 본문}
		ex){'content_names': 317, 'content_dates': '2016-07-20 16:01', 'content_link': ['http://ppss.kr/archives/66089'], 'content_coms': '당장 느끼는 기분이 행복을 결정하지는 않습니다 | ㅍㅍㅅㅅ - http://ppss.kr/archives/66089'} 입니다.
  
