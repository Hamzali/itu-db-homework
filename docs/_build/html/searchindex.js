Search.setIndex({docnames:["config","constants","controllers","errors","index","middlewares","models","modules","server","utils"],envversion:53,filenames:["config.rst","constants.rst","controllers.rst","errors.rst","index.rst","middlewares.rst","models.rst","modules.rst","server.rst","utils.rst"],objects:{"":{config:[0,0,0,"-"],constants:[1,0,0,"-"],controllers:[2,0,0,"-"],errors:[3,0,0,"-"],middlewares:[5,0,0,"-"],models:[6,0,0,"-"],server:[8,0,0,"-"],utils:[9,0,0,"-"]},"config.Config":{CSRF_ENABLED:[0,2,1,""],DEBUG:[0,2,1,""],SECRET_KEY:[0,2,1,""],SQLALCHEMY_DATABASE_URI:[0,2,1,""],TESTING:[0,2,1,""]},"config.DevelopmentConfig":{DEBUG:[0,2,1,""],DEVELOPMENT:[0,2,1,""]},"config.ProductionConfig":{DEBUG:[0,2,1,""]},"config.StagingConfig":{DEBUG:[0,2,1,""],DEVELOPMENT:[0,2,1,""]},"config.TestingConfig":{TESTING:[0,2,1,""]},"controllers.chatGroup":{leave_chatgroup:[2,3,1,""],show_groups:[2,3,1,""],students_group:[2,3,1,""]},"controllers.comments":{comments:[2,3,1,""],getCommentsOfStudent:[2,3,1,""]},"controllers.courses":{building_by_id:[2,3,1,""],faculties_by_id:[2,3,1,""],list_buildings:[2,3,1,""],list_courses:[2,3,1,""],list_faculties:[2,3,1,""],list_one_course:[2,3,1,""],sync_buildings:[2,3,1,""],sync_courses:[2,3,1,""],sync_faculties:[2,3,1,""]},"controllers.homeworks":{homework:[2,3,1,""]},"controllers.lecturers":{lecturer:[2,3,1,""],show_a_lecturer:[2,3,1,""]},"controllers.students":{enroll_course:[2,3,1,""],join_study_group:[2,3,1,""],list_student_courses:[2,3,1,""],list_student_studygroups:[2,3,1,""],one_student:[2,3,1,""],student_login:[2,3,1,""],student_logout:[2,3,1,""]},"controllers.studygroups":{check_study_group:[2,3,1,""],find_studygroups_of_student:[2,3,1,""],find_update_studygroup:[2,3,1,""],list_studygroup_students:[2,3,1,""],list_studygroups:[2,3,1,""],set_student_studygroup_status:[2,3,1,""]},"models.base_model":{BaseModel:[6,1,1,""],db_factory_func:[6,3,1,""]},"models.base_model.BaseModel":{"delete":[6,5,1,""],create:[6,5,1,""],delete_by_id:[6,5,1,""],find:[6,5,1,""],find_by_id:[6,5,1,""],find_one:[6,5,1,""],update:[6,5,1,""],update_by_id:[6,5,1,""]},"models.buildings":{BuildingModel:[6,1,1,""],CourseBuildingModel:[6,1,1,""]},"models.chatGroup":{ChatGroupsModel:[6,1,1,""],StudentsOnChatModel:[6,1,1,""]},"models.chatGroup.ChatGroupsModel":{checkIsAdmin:[6,5,1,""],createGroup:[6,5,1,""],getLastGroupCreatedById:[6,5,1,""],listGroups:[6,5,1,""],removeGroup:[6,5,1,""],updateGroup:[6,5,1,""]},"models.chatGroup.StudentsOnChatModel":{addMember:[6,5,1,""],checkIfMember:[6,5,1,""],listMembersOfGroup:[6,5,1,""],removeMember:[6,5,1,""],showGroupsOfStudent:[6,5,1,""]},"models.comments":{CommentsModel:[6,1,1,""]},"models.comments.CommentsModel":{addComment:[6,5,1,""],removeComment:[6,5,1,""],showCommentsOfStudent:[6,5,1,""],updateComment:[6,5,1,""]},"models.courses":{CourseModel:[6,1,1,""],StudentCourseModel:[6,1,1,""]},"models.courses.CourseModel":{course_exists:[6,5,1,""]},"models.courses.StudentCourseModel":{delete_student_course:[6,5,1,""],find_student_courses:[6,5,1,""]},"models.faculties":{FacultyModel:[6,1,1,""]},"models.homeworks":{HomeworksModel:[6,1,1,""],HomeworksOfStudentModel:[6,1,1,""]},"models.homeworks.HomeworksModel":{addHomework:[6,5,1,""],changeHomework:[6,5,1,""],getLastHwCreatedById:[6,5,1,""],listHomeworks:[6,5,1,""],removeHomework:[6,5,1,""]},"models.homeworks.HomeworksOfStudentModel":{addHomeworkOfStudent:[6,5,1,""],removeStudentsHomework:[6,5,1,""],showHomeworks:[6,5,1,""]},"models.lecturers":{LecturersModel:[6,1,1,""]},"models.lecturers.LecturersModel":{addLecturer:[6,5,1,""],listAllLecturers:[6,5,1,""],listAllLecturersBySName:[6,5,1,""],listLecturersOfDepartment:[6,5,1,""],removeLecturer:[6,5,1,""],showALecturer:[6,5,1,""],updateLecturer:[6,5,1,""]},"models.students":{StudentModel:[6,1,1,""]},"models.students.StudentModel":{remove_token:[6,5,1,""],validate_token:[6,5,1,""]},"models.studygroups":{StudentStudyGroup:[6,1,1,""],StudyGroupModel:[6,1,1,""]},"models.studygroups.StudentStudyGroup":{find_student_studygroups:[6,5,1,""],list_studygroup_students:[6,5,1,""],list_studygroups_of_student:[6,5,1,""],set_student_status:[6,5,1,""]},"models.studygroups.StudyGroupModel":{get_available_study_groups:[6,5,1,""]},config:{Config:[0,1,1,""],DevelopmentConfig:[0,1,1,""],ProductionConfig:[0,1,1,""],StagingConfig:[0,1,1,""],TestingConfig:[0,1,1,""]},controllers:{chatGroup:[2,0,0,"-"],comments:[2,0,0,"-"],courses:[2,0,0,"-"],homeworks:[2,0,0,"-"],lecturers:[2,0,0,"-"],students:[2,0,0,"-"],studygroups:[2,0,0,"-"]},errors:{DataBaseException:[3,4,1,""]},middlewares:{auth_func:[5,3,1,""]},models:{base_model:[6,0,0,"-"],buildings:[6,0,0,"-"],chatGroup:[6,0,0,"-"],comments:[6,0,0,"-"],courses:[6,0,0,"-"],faculties:[6,0,0,"-"],homeworks:[6,0,0,"-"],lecturers:[6,0,0,"-"],students:[6,0,0,"-"],studygroups:[6,0,0,"-"]},server:{root_path_handler:[8,3,1,""]},utils:{int_to_datetime:[9,3,1,""],time_to_json:[9,3,1,""]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","function","Python function"],"4":["py","exception","Python exception"],"5":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:function","4":"py:exception","5":"py:method"},terms:{"class":[0,6],"new":[2,6],"return":[2,6],"throw":3,"true":0,Used:6,With:2,_id:6,about:6,add:[2,6],addcom:6,added:2,addhomework:6,addhomeworkofstud:6,adding:6,addlectur:6,addmemb:6,admin:6,all:[2,6],allow:[2,6],alter:[2,6],anyth:6,api:2,applic:3,attribut:3,aurl:0,auth:2,auth_func:5,authent:[2,5,6],avail:[2,6],backend:4,base:[0,3,6],base_model:7,basemodel:6,between:6,bind:2,bodi:2,build:[2,7],building_by_id:2,buildingid:2,buildingmodel:6,caller:2,chang:[0,6],changehomework:6,chat:[2,6],chatgroup:7,chatgroupsmodel:6,check:[2,6],check_study_group:2,checkifmemb:6,checkisadmin:6,cid:2,comment:7,commentsmodel:6,config:[4,7],conn:6,connect:6,constant:[4,7],contain:[2,6],content:[4,7],control:[4,7],cours:7,course_exist:6,coursebuildingmodel:6,courseid:[2,6],coursemodel:6,crawl:2,creat:[2,6],creategroup:6,crn:2,crud:6,csrf_enabl:0,current:2,data:[2,6,9],databas:[2,3,6],databaseexcept:3,date:9,date_end:6,date_start:6,db_factory_func:6,debug:0,decarotor:5,decor:[2,6],delet:[2,6],delete_by_id:6,delete_student_cours:6,depart:[2,6],detail:6,develop:0,developmentconfig:0,dictionari:6,element:6,endpoint:2,enrol:2,enroll_cours:2,error:[4,7],except:3,exclud:2,exist:6,explan:3,faculti:[2,7],faculties_by_id:2,facultyid:2,facultymodel:6,fals:[0,6],featur:6,field:[6,9],find:[2,6],find_by_id:6,find_on:6,find_student_cours:6,find_student_studygroup:6,find_studygroups_of_stud:2,find_update_studygroup:2,form:[2,6],format:9,from:[2,6],func:6,get:2,get_available_study_group:6,getcommentsofstud:2,getlastgroupcreatedbyid:6,getlasthwcreatedbyid:6,given:[2,6],group:[2,6],groupid:2,has:6,homework:7,homeworksmodel:6,homeworksofstudentmodel:6,hwid:6,ident:6,ids:6,implement:6,includ:2,index:4,inform:[2,6],init_t:6,initi:6,insert:6,instanc:9,int_to_datetim:9,integ:9,itu:2,join:[2,6],join_study_group:2,json:[2,9],just:6,keep:6,last:6,leav:2,leave_chatgroup:2,lectur:7,lecturersmodel:6,lid:2,limit:6,list:2,list_build:2,list_cours:2,list_faculti:2,list_one_cours:2,list_student_cours:2,list_student_studygroup:2,list_studygroup:2,list_studygroup_stud:[2,6],list_studygroups_of_stud:6,listalllectur:6,listalllecturersbysnam:6,listgroup:6,listhomework:6,listlecturersofdepart:6,listmembersofgroup:6,log:2,logout:2,make:2,manipul:6,member:[2,6],membership:6,messag:3,method:[2,6],middlewar:[4,7],model:[4,7],modul:[4,7],need:0,none:6,number:2,object:[0,2,6,9],offset:6,one:[2,6],one_stud:2,oper:6,order:9,out:2,own:2,owner:6,packag:[4,7],page:4,pagin:2,param:2,paramet:[2,9],pars:9,particip:2,password:2,pin:2,post:2,prefer:2,primary_kei:6,productionconfig:0,put:2,queri:[2,6],rais:3,realli:0,relat:6,remov:[2,6],remove_token:6,removecom:6,removegroup:6,removehomework:6,removelectur:6,removememb:6,removestudentshomework:6,request:2,rest:[2,4],retriev:[2,6],return_col:6,room:2,root_path_handl:8,rout:2,row:6,search:4,secret_kei:0,see:6,server:[4,7],set_student_statu:6,set_student_studygroup_statu:2,show:2,show_a_lectur:2,show_group:2,showalectur:6,showcommentsofstud:6,showgroupsofstud:6,showhomework:6,sid:2,simulten:6,sort_bi:6,sourc:[0,2,3,5,6,8,9],specif:[2,3,6],sqlalchemy_database_uri:0,stagingconfig:0,statu:[2,6],store:6,string:2,student:[5,7],student_login:2,student_logout:2,student_model:5,studentcoursemodel:6,studentid:[2,6],studentmodel:6,students_group:2,studentsonchatmodel:6,studentstudygroup:6,studi:[2,6],study_end:2,study_start:2,studygroup:7,studygroupid:[2,6],studygroupmodel:6,submodul:7,sync:2,sync_build:2,sync_cours:2,sync_faculti:2,tabl:6,test:[0,6],testingconfig:0,text:2,thi:[0,6],time:[2,9],time_to_json:9,timestamp:[2,9],token:6,track:6,unknown:6,updat:[2,6],update_by_id:6,updatecom:6,updategroup:6,updatelectur:6,user:[2,6],usernam:2,util:[4,7],validate_token:6,websit:2,where:6,wheter:6,which:6,write:2},titles:["config module","constants module","controllers package","errors module","Welcome to Itunder\u2019s documentation!","middlewares module","models package","itunder-backend-rest","server module","utils module"],titleterms:{backend:7,base_model:6,build:6,chatgroup:[2,6],comment:[2,6],config:0,constant:1,content:[2,6],control:2,cours:[2,6],document:4,error:3,faculti:6,homework:[2,6],indic:4,itund:[4,7],lectur:[2,6],middlewar:5,model:6,modul:[0,1,2,3,5,6,8,9],packag:[2,6],rest:7,server:8,student:[2,6],studygroup:[2,6],submodul:[2,6],tabl:4,util:9,welcom:4}})