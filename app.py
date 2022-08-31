#!env/bin/python
from flask.app import Flask

from logic.apps.admin.config.app import setup_id_agent
from logic.apps.admin.config.logger import setup_loggers
from logic.apps.admin.config.rest import setup_rest
from logic.apps.admin.config.variables import Vars, setup_vars
from logic.apps.jaime.services.jaime_service import connect_with_jaime
from logic.libs.logger.logger import logger
from logic.libs.variables.variables import get_var

setup_vars()
setup_loggers()

app = Flask(__name__)
setup_rest(app)

id_agent = setup_id_agent()
logger().info(f'Agent ID -> {id_agent}')
connect_with_jaime()

logger().info("""

                        ^Y?:    7J!.                                                                                                                                                
                        7##BPJ!^P#BGY!:                                                                                                                                             
                    .^!7YBBB###BBBB##BGPYJ?!^:                                                                ..:::^:.                                                              
                 :75GB###BBBBBBBBBBBBB#####BBG5?^                                                        .:^^^^^~^^:.                                                               
               ^YB###BBBBBBBBBBBBBBBBBBBBBBBBBBBG5!                                                   .:^^:...:^.                                                                   
              ?B#BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGB5:                                               :^:.    :~~.                                                                    
             Y#BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGP:                                            .^:      :~~.                                                                     
            7#BBBBBBBBGGGGBBBBBBBBBBBBBBBGGGBBBBBBGGB5                                           ::       :~~:                                                                      
            5#BBBBBBBBGGGGGGGGGGGGGGGGGGGGGGBBBBBBGGGG:                                         ^.       .~~^                           ..                                          
            P#BBBBBBBBBGGGGGGGGGGGGGGGGGGGGGBBBBBBGGGG^                                        :.        ^~~.                         .^:                                           
            P#BBBBBBBBBGGGGGGGGGGGGGGGGGGGGGBBBBBBGGGG^                                        ^        :~~^                         ^^                                             
            P#BBBBBBBG5J????YGGGGGGGGGGGGGGGGGPGGBGGGG^                                       .^       .~~^                          .                                              
            P#BBBBGGG?!J555Y!75GGGGGGGGGPGGGGP55PBGGGG^                                        ::      ^~~.       ...::::.:^.      .:.   ..:^:  .::^^.   .::^^.       .::^^:.       
            P#BBBBGGY~?B5~JBY~?GGGGGGGGP~?GGGP55GBGGGG^                                         ::.   :~~:     .::.     ^~~:    .:~~^   ...~~^.:...~~^ ::. :~~^     :^.. :~~^       
            PBBGGBBGP7!J55PY7!5GGGGGGGGGPGGGGP55BBGGGG^                        .......            ...^~~:.    :~^      :~~.     .^~^      :~~^:   .~~^:.   ^~^     ^~.  .:^^.       
           ^PPPPPGBGGG5?777?YPGGGGGGGGGGGGGGGP5GBPPPPP7                    ..::..                   :~^.     ^~^     .^~~:      ^~^      .~~^.    ^~~:    :~~.    ^~^.....          
           JPPPPPPBBBGGG57JGBBBBBBBBBBGGGGGGGGB#GPPPPPP:                 .^:.                      :~^      :~~^    :^~~^      ^~~.      ^~^.    :~~:    .~~.    :~~:               
           :YPPPPPG#BBBG57YBBBBBBBBBBBBBGGGGBB#BPPPPP5!                .^^.                       ^~:       :~~^..::..~~^ .:  .~~^ .:.  ^~~.    :~~:     ^~~. :. :~~^.  ..:.        
             :^^!J7?B#BB57Y#BBGGGGGGBBBBBBBB##5~^^^^:.                :~^                       :~^.         :^^^:.   ^^^:.    ^^^:.   .^^.    .^^:      :^^^:.   :^^^^::.          
                :?~ ~P##P7Y#BBBBBBBBBBBBBB##G?                       :~~:                     .^^.                                                                                  
                .77^  !5J?G#BBBBBBBBBBB##BP7.                        ^~~:                   .::.                                                                                    
                 .~!7!!!~^?GBBBBBBBBBBBY7:                           :~~~:              ..:::                                                                                       
                       .:^:JPGGGGGGGGPP~^^.                           :^~~^:.........::::.                                                                                          
                   .:~!J?!!!7?JYYY5YJ?7!!7Y7^:.                         ..::^::::::...                                                                                              
                 :!?JJYY7^~~~^~!!!!!~^~~~~YYJ7!~:                                                                                                                                   
               .!JJJYYYYY!~~~~!!!!!!~~~~~JYYYY7!!~.                                                                                                                                 
               7J?JYYYYY?~~~~^~!!!!!~^~~~!YYYYY?!!!:                                                                                                                                
              ~J?JYYYYYY7~~~!?YP55P5J7~~~!YYYYYY?!!~                                                                                                                                
              !J?JJJJYYYYYJJG&&&5J#@&#YJJYYYYYJJ7!!!.                                                                                                                               
              !J???JYYYYYYYYG&&&#B&&&#5YYYYYYYJ?7!!!.                                                                                                                               
              !J???JYYYYYYYYG&&&5J#&&#YYYYYYYYJJ7!!!.                                                                                                                               
              !J?????JJYYYYYG&&&BB&&&#YYYYYJJ??J7!!!.                                                                                                                               
              !J????????JYYYB&&&&&&&&#5YYJJ???JJ7!!!.                                                                                                                       
                                                                                                                                                                        
""")


if __name__ == "__main__":
    flask_host = get_var(Vars.PYTHON_HOST)
    flask_port = int(get_var(Vars.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=False)
