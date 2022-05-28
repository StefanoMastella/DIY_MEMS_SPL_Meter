#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mtslazarin

Editted by Stéfano (26/05/2022)
"""
# %% Initializing

import pytta
from pytta import roomir as rmr
import os

# %% Muda o current working directory do Python para a pasta onde este script
# se encontra

cwd = os.path.dirname(__file__) # Pega a pasta de trabalho atual
os.chdir(cwd)

tempHumid = None  # Para testes com LabJack offline
fs = 44100

# %% Carrega sinais de excitação e cria dicionário para o setup da medição

excitationSignals = {}
excitationSignals['varredura18'] = pytta.generate.sweep(
        # Geração do sweep (também pode ser carregado projeto prévio)
        freqMin=100,
        freqMax=10000,
        fftDegree=18,
        startMargin=0.05,
        stopMargin=1,
        method='logarithmic',
        windowing='hann',
        samplingRate=fs)

excitationSignals['varredura17'] = pytta.generate.sweep(
        # Geração do sweep (também pode ser carregado projeto prévio)
        freqMin=20,
        freqMax=20000,
        fftDegree=17,
        startMargin=0.05,
        stopMargin=1,
        method='logarithmic',
        windowing='hann',
        samplingRate=fs)

# %% Cria novo setup de medição e inicializa objeto de dados, o qual gerencia o
# MeasurementSetup e os dados da medição em disco

MS = rmr.MeasurementSetup(name='Meas 01',  # Nome da medição
                          samplingRate=fs,  # [Hz]
                          # Interface de áudio
                          # Sintaxe : device = [<in>,<out>] ou <in/out>
                          # Utilize pytta.list_devices() para listar
                          # os dispositivos do seu computador.
                          device=[1,10], # PC Stéfano
                          noiseFloorTp=5,  # [s] tempo de gravação do ruído de fundo
                          calibrationTp=2,  # [s] tempo de gravação do sinal de calibração
                          excitationSignals=excitationSignals,  # Sinais de excitação
                          
                          # Número de médias por tomada de medição: para grande
                          # número de médias recomenda-se dividi-las em algumas
                          # tomadas distintas.
                          averages=2,  
                          pause4Avg=True,  # Pausa entre as médias
                          freqMin=100,  # [Hz]
                          freqMax=10000,  # [Hz]
                          
                          # Dicionário com canais de saída, códigos associados
                          # e grupos de canal (arranjos)
                          inChannels={'Mic1': (1, 'Mic 1'),
                                      'Mic2': (2, 'Mic 2')},
                          # Dicionário com códigos dos canais e compensações
                          # associadas à cadeia de entrada
                          # inCompensations={'Mic1': (mSensFreq, mSensdBMag)},
                          inCompensations={},
                          
                          # Dicionário com códigos e canais de saída associados
                          outChannels={'O1': (1, 'Dodecaedro 1')},
                          # Dicionário com códigos dos canais e compensações
                          # associadas à cadeia de saída
                          # outCompensations={'O2': (sSensFreq, sSensdBMag)})
                          outCompensations={})
D = rmr.MeasurementData(MS)

# %% Cria nova tomada de medição

takeMeasure = rmr.TakeMeasure(MS=MS,
                              # Passa objeto de comunicação
                              # com o LabJack U3 + EI1050 probe
                              tempHumid=tempHumid,
                              kind='roomres',
                              inChSel=['Mic2'],
                              receiversPos=['R1'],
                              # Escolha do sinal de excitação
                              # disponível no Setup de Medição
                              excitation='varredura18',
                              # Código do canal de saída a ser utilizado.
                              outChSel='O1',
                              # Ganho na saída
                              outputAmplification=-3, # [dB]
                              # Configuração sala-fonte-receptor
                              sourcePos='S1')

# %% Cria nova tomada de medição do ruído de fundo

takeMeasure = rmr.TakeMeasure(MS=MS,
                              # Passa objeto de comunicação
                              # com o LabJack U3 + EI1050 probe
                              tempHumid=tempHumid,
                              kind='noisefloor',
                              inChSel=['Mic1','Mic2'],
                              receiversPos=['R1','R1'])

# %% Cria nova tomada de medição para recalibração de fonte

takeMeasure = rmr.TakeMeasure(MS=MS,
                              tempHumid=tempHumid,
                              kind='sourcerecalibration',
                              # Lista com códigos de canal individual ou
                              # códigos de grupo
                              inChSel=['Mic1'],
                              # Escolha do sinal de excitação
                              # disponível no Setup de Medição
                              excitation='varredura18',
                              # Código do canal de saída a ser utilizado.
                              outChSel='O2',
                              # Ganho na saída
                              outputAmplification=-6) # [dB]

# %% Cria nova tomada de medição para calibração do microfone

takeMeasure = rmr.TakeMeasure(MS=MS,
                              tempHumid=tempHumid,
                              kind='miccalibration',
                              # Lista com códigos de canal individual ou
                              # códigos de grupo
                              inChSel=['Mic1'])

# %% Cria nova tomada de medição para calibração de canal

takeMeasure = rmr.TakeMeasure(MS=MS,
                              tempHumid=tempHumid,
                              kind='channelcalibration',
                              # Lista com códigos de canal individual ou
                              # códigos de grupo
                              inChSel=['Mic1'],
                              # Escolha do sinal de excitação
                              # disponível no Setup de Medição
                              excitation='varredura17',
                              # Código do canal de saída a ser utilizado.
                              outChSel='O1',
                              # Ganho na saída
                              outputAmplification=-30) # [dB]

# %% Inicia tomada de medição/aquisição de dados

takeMeasure.run() 

# %% Salva tomada de medição no disco

D.save_take(takeMeasure)
