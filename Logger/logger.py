#!/usr/bin/python
# -*- coding: utf8 -*-
import logging


def setup_logger(logger_name, log_file, level=logging.DEBUG): #.INFO
    lz = logging.getLogger(logger_name)
    
    #formatter = logging.Formatter('%(asctime)s : %(message)s')
    formatter =logging.Formatter('Date-Time : %(asctime)s : Line No. : %(lineno)d - %(name)s- %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    lz.setLevel(level)
    lz.addHandler(fileHandler)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    lz.addHandler(streamHandler) #-> si se activa sale por pantalla
    
    
def setup_logger2(logger_name, log_file, consoleLevel=logging.DEBUG,fileLevel=logging.DEBUG):
    lz = logging.getLogger(logger_name)
    # Create handlers
    #Console
    consoleHandler=logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter('%(name)s - %(message)s'))
    consoleHandler.setLevel(consoleLevel)


    #File
    log_file=log_file
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(logging.Formatter('Date-Time : %(asctime)s : Line No. : %(lineno)d - %(name)s- %(process)d - %(levelname)s - %(message)s'))
    fileHandler.setLevel(fileLevel)

    lz.addHandler(consoleHandler)
    lz.addHandler(fileHandler)

    lz.debug("test mensaje debug")
    lz.info("test mensaje info")
    lz.warning("test mensaje warning")
    lz.critical("test mensaje critical")
    
    #los unicos mensajes que se graban son de nivel warning para arriba