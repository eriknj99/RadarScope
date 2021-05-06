#!/bin/bash

mpv --gpu-context=x11egl --gpu-hwdec-interop=vaapi-egl --hwdec=vaapi $1
