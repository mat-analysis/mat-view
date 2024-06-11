import os
from dash import html
from abc import ABC

class BaseMethod(ABC):
    
    PROVIDE = '' # This should be the unique code for the method
    
    def __init__(self, idx):
        self.idx = idx
        
    @staticmethod
    def wrappers():
        return dict(map(lambda cls: (cls.__name__, cls), BaseMethod.__subclasses__()))
    
    @staticmethod
    def providedMethods():
        return dict(map(lambda cls: (cls[1].PROVIDE, cls[1]), BaseMethod.wrappers().items()))
    
    @property
    def name(self):
        return self.PROVIDE
        
    def title(self):
        return self.NAMES[self.PROVIDE]
    
    def render(self):
        return [
            html.I(html.P("Method "+self.NAMES[self.PROVIDE]+" has default configuration.")),
        ]
    
    def generate(self, params, base, data=None, dataset=None, check_done=True):
        
        results = os.path.join('${BASE}', 'results', dataset)
        prog_path = os.path.join('${BASE}', 'programs')
        if not data:
            data = os.path.join('${BASE}', 'data', dataset)
        
        sh =  '#!/bin/bash\n'
        sh += '# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- \n'    
        sh += '# '+ self.title() +'\n'
        sh += '# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- \n'    
        sh += '# # # CONFIGURATIONS # # #\n'
        sh += 'BASE="'+base+'"\n'
        sh += 'DATAPATH="'+data+'"\n'
        sh += 'PROGPATH="'+prog_path+'"\n'
        sh += 'RESPATH="'+results+'"\n'
        sh += 'DIR="'+self.name+'"\n'
        sh += '\n'
        sh += '# # # BEGIN generated script # # #\n'
        
        data_path = '${DATAPATH}'
        res_path  = '${RESPATH}'
        prog_path = '${PROGPATH}'
        name = '${DIR}'
        
        if 'k' in params.keys():
            sh += '# Running '+str(params['k'])+'-fold experiments:\n'
            k = params['k'] if isinstance(params['k'], list) else list(range(1, params['k']+1))
            sh += 'for RUN in '+ ' '.join(['"run'+str(x)+'"' for x in k]) + '\n'
            sh += 'do\n'
            sh += '\n'
            
            data_path=os.path.join('${DATAPATH}','${RUN}')
            
        exp_path = os.path.join(res_path, name) # '${NAME}')

        if check_done:
            sh += '# Check if experiment was already done:\n'
            sh += 'if [ -d "'+exp_path+'" ]; then\n'
            sh += '   echo "'+exp_path+' ... [Is Done]"\n'
            sh += 'else\n'
            sh += '\n'
        
        sh += '# Create result directory:\n'
        sh += 'mkdir -p "'+exp_path+'"\n'
        sh += '\n'
        
        sh += '# Run method:\n'
        sh += self.script(dict(params, **{'dataset': dataset}), folder=name, data_path=data_path, res_path=res_path, prog_path=prog_path)

        sh += '\n'
        sh += 'echo "'+exp_path+' ... Done."\n'
        if check_done:
            sh += 'fi\n'
        if 'k' in params.keys():
            sh += 'done\n'
        sh += '# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- \n'      
        sh += '# # # END generated script # # #'
        
        return sh
    
    def downloadLine(self):
        return ''

class TrajectoryBaseMethod(ABC):

    def __init__(self):
        pass
        
    def script(self, params, folder='${DIR}', data_path='${DATAPATH}', res_path='${RESPATH}', prog_path='${PROGPATH}'):
        outfile = os.path.join(res_path, folder, folder+'.txt')
        
        cmd = f'MAT-TC.py -c "{self.PROVIDE}" "{data_path}" "{res_path}"'
        if 'TC' in params.keys():
            cmd = 'timeout ' + params['TC'] +' '+ cmd
        
        cmd += f' 2>&1 | tee -a "{outfile}" \n\n'
        
        cmd += '# This script requires python package "mat-classification".\n'
        
        return cmd
    

class MoveletsBaseMethod(ABC):
    def __init__(self, isLog=None, isPivots=None, isTau=None, tau=None, isLambda=None):    
        self.isLog = isLog
        
        self.isPivots = isPivots
        
        self.isTau = isTau
        self.tau = tau
        self.temp_tau = tau
        
        self.isLambda = isLambda
    
    @property
    def name(self):
        name = self.PROVIDE
        if self.isPivots:
            name += 'p'
        if self.isLog:
            name += 'L'
        if self.isLambda:
            name += 'D'
        if self.isTau and self.tau != 0.9:
            name += 'T{}'.format(int(self.tau*100))
        return name
    
    def title(self):
        name = self.NAMES[self.PROVIDE]
        if self.isPivots:
            name += 'Pivots'
        else:
            name += 'Movelets'
        if self.isLog:
            name += '-Log'
        if self.isLambda:
            name += '-λ'
        if self.isTau and self.tau and self.tau != 0.9:
            name += ' τ={}%'.format(int(self.tau*100))
        return name
        
    @property
    def version(self):
        cmd = ' -version ' + self.PROVIDE
        if self.isPivots:
            cmd += '-pivots'
        return cmd
    
    @property
    def jar_name(self):
        return 'MoveletDiscovery.jar'
    
    @property
    def classifiers(self):
        return 'MMLP,MRF,MSVC'
    
    
    def desc_file(self, params):
        return params['dataset'] + ".json"
    
    def cmd_line(self, params):
        # 0-java_opts; 1-program; 2-data_path; 3-res_path; 4-config; 5-extras
        return 'java {0} -jar "{1}" -curpath "{2}" -respath "{3}" {4} {5}'
    
    def extras(self, params):
        if 'TC' in params.keys():
            return '-tc ' + params['TC']
        return ''
    
    def cmd_nt(self, params):
        if 'nt' in params.keys():
            return f" -nt {params['nt']}"
        return ''
    def cmd_log(self, params):
        if not self.isLog:
            return ' -Ms -1'
        else:
            return ' -Ms -3'
    def cmd_pivots(self, params):
        return ''
    def cmd_tau(self, params):
        if self.isTau:
            return ' -TR ' + str(self.tau) # only TR (Relative Tau), the -TF (for fixed Tau) is Deprecated
        return ''
    def cmd_lambda(self, params):
        if self.isLambda:
            return ' -Al true'
        return ''
    
    def script(self, params, folder='${DIR}', data_path='${DATAPATH}', res_path='${RESPATH}', prog_path='${PROGPATH}'):
        
        program = os.path.join(prog_path, self.jar_name)
        exp_path = os.path.join(res_path, folder)
        
        outfile = os.path.join(res_path, folder, folder+'.txt')
        
        java_opts = ''
        if 'GB' in params.keys():
            java_opts = f"-Xmx{int(params['GB'])}G"
            
        descriptor = os.path.join(data_path, self.desc_file(params))
        cmd = f'-descfile "{descriptor}"'
        
        cmd += self.version
#        if self.isPivots:
        cmd += self.cmd_pivots(params)
        cmd += self.cmd_nt(params)
        cmd += self.cmd_log(params)
        cmd += self.cmd_tau(params)
        cmd += self.cmd_lambda(params)
        
#        if 'nt' in params.keys():
#            cmd += f" -nt {params['nt']}"
#            
#        if not self.isLog:
#            cmd += ' -Ms -1'
#        else:
#            cmd += ' -Ms -3'
#            
#        if self.isTau:
#            cmd += ' -TR ' + str(self.tau) # only TR (Relative Tau), the -TF (for fixed Tau) is Deprecated
#            
#        if self.isLambda:
#            cmd += ' -Al true'
        
#        f'java {java_opts} -jar "{program}" -curpath "{data_path}" -respath "{res_path}" ' + cmd
        cmd = self.cmd_line(params).format(java_opts, program, data_path, exp_path, cmd, self.extras(params))
        
        cmd += f' 2>&1 | tee -a "{outfile}" \n\n'
        
        cmd += '# Join the result train and test data:\n'
        cmd += f'MAT-MergeDatasets.py "{exp_path}" \n\n'
        
        cmd += '# Run MLP and RF classifiers:\n'
        cmd += f'MAT-MC.py -c "{self.classifiers}" -m "{folder}" "{exp_path}"\n\n'
        
        cmd += '# This script requires python package "mat-classification".\n'
        
        return cmd
    
    def downloadLine(self):
        url = 'https://raw.githubusercontent.com/mat-analysis/mat-classification/main/jarfiles'
        model = 'curl -o {1} {0}/{1} \n'
        return model.format(url, self.jar_name)