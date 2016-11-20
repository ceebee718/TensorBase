#!/usr/bin/env python

"""
Author: Dan Salo
Last Edit: 11/11/2016

Purpose: Parent Class for all models creation
Example:
    x ### is a numpy 4D array
    encoder = Layers(input)
    encoder.conv2d(3, 64)
    encoder.conv2d(3, 64)
    encoder.maxpool()
    ...
    decoder = Layers(z)
    decoder.deconv2d(4, 156, padding='VALID')
    decoder.deconv2d(3, 144, stride=2)
    decoder.deconv2d(5, 128, stride=2)
    ...
"""

import tensorflow as tf
import numpy as np
import logging
import os
import datetime


class Models:
    def __init__(self, flags, model_num):
        print(flags)
        self.model_num = model_num
        self.flags = self._check_flags(flags)
        self._check_file_io(model_num)
        self._set_placeholders()
        self._set_seed()
        self._set_summaries()

        self._network()
        self._optimizer()

        self.merged, self.saver, self.sess, self.writer = self._set_tf_functions()
    
    def _set_placeholders(self):
        # Define placeholder
    
    def _network(self):
        # Define network

    def _optimizer(self):
        # Define optimizer

    def _load_data_class(self, image_dict):
        # run an instance of Data Class

    def _generate_training_batch(self):
        # Use instance of Data class to generate training batch

    def _run_training_iter(self):
        # run sess.run on optimizer

    def _run_training_summary_iter(self):
        # run sess.run on optimizer and merged summaries

    def _record_metrics(self):
        # Define and save metrics

    def _check_flags(self, flags):
        flags_keys = ['data_directory', 'model_directory', 'datasets', 'restore', 'restore_file', 'batch_size',
                      'display_step', 'weight_decay', 'lr_decay', 'lr_iters']
        for k in flags_keys:
            try:
                flags[k]
            except KeyError:
                print('The key %s is not defined in the flags dictionary. Please define and run again' % k)
        return flags

    def _check_file_io(self, model_num):
        folder = 'Model' + str(model_num) + '/'
        self.flags['restore_directory'] = self.flags['save_directory'] + self.flags['model_directory']
        self.make_directory(self.flags['restore_directory'])
        self.flags['logging_directory'] = self.flags['restore_directory'] + folder
        self.make_directory(self.flags['logging_directory'])
        logging.basicConfig(filename=self.flags['logging_directory'] + 'ModelInformation.log', level=logging.INFO)

    def _set_seed(self):
        tf.set_random_seed(self.flags['seed'])
        np.random.seed(self.flags['seed'])

    def _set_summaries(self):
        for var in tf.trainable_variables():
            tf.histogram_summary(var.name, var)

    def _set_tf_functions(self):
        return tf.merge_all_summaries(), tf.train.Saver(), tf.InteractiveSession(),\
               tf.train.SummaryWriter(self.flags['logging_directory'], self.sess.graph)

    def _restore(self):
        self.saver.restore(self.sess, self.flags['restore_directory'] + self.flags['restore_file'])
        self.print_log("Model restored from %s" % self.flags['restore_file'])

    def _setup_metrics(self):
        self.print_log('Date: ' + str(datetime.datetime.now()).split('.')[0])
        datasets = 'Datasets: '
        for d in self.flags['datasets']:
            datasets += d + ', '
        self.print_log(datasets)
        self.print_log('Batch_size: ' + self.check_str(self.flags['batch_size']))
        self.print_log('Model: ' + self.check_str(self.flags['model_directory']))
        for l in range(len(self.flags['lr_iters'])):
            self.print_log('EPOCH %d' % l)
            self.print_log('Learning Rate: ' + str(self.flags['lr_iters'][l][0]))
            self.print_log('Iterations: ' + str(self.flags['lr_iters'][l][1]))

    def _initialize_training(self):
        self._setup_metrics()
        if self.flags['restore'] is True:
            self._restore()
        else:
            self.sess.run(tf.initialize_all_variables())
            self.print_log("Model training from scratch.")

    def _save_model(self, epoch_num):
        self.print_log("Optimization Finished!")
        checkpoint_name = self.flags['logging_directory'] + 'Model' + self.check_str(self.model_num) + 'epoch_%d' % epoch_num + '.ckpt'
        save_path = self.saver.save(self.sess, checkpoint_name)
        self.print_log("Model saved in file: %s" % save_path)

    def _record_training_step(self, summary, step, global_step):
        self.writer.add_summary(summary=summary, global_step=global_step)
        step += 1
        global_step += 1

    def train(self):
        self._initialize_training()
        self.global_step = 1
        for i in range(len(self.flags['lr_iters'])):
            lr = self.flags['lr_iters'][i][0]
            iters_num = self.flags['lr_iters'][i][1]
            self.print_log('Learning Rate: %d' % lr)
            self.print_log('Iterations: %d' % iters_num)
            self.step = 1
            while self.step < iters_num:
                print('Batch number: %d' % step)
                self._generate_training_batch()
                if step % self.flags['display_step'] != 0:
                    self._run_training_iter()
                else:
                    self._run_training_summary_iter()
                    self._record_metrics()
                self._record_training_step(step, global_step)
            self._save_model(epoch_num=i)

    @staticmethod
    def make_directory(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    @staticmethod
    def print_log(message):
        print(message)
        logging.info(message)

    @staticmethod
    def check_str(obj):
        if isinstance(obj, str):
            return obj
        if isinstance(obj, float):
            return str(int(obj))
        else:
            return str(obj)