#!/bin/bash

if [ -d "package" ]; then
    rm -rf package/*
fi

for stage in {0..3}; do
    mkdir -p package/Stage${stage}/sources
    mkdir -p package/Stage${stage}/bin

    # Stage${stage}
    pyinstaller --onefile Stage${stage}/client/client_runner.py && pyinstaller --onefile Stage${stage}/server/server_runner.py
    cp Stage${stage}/client/client.py package/Stage${stage}/sources
    cp Stage${stage}/server/server.py package/Stage${stage}/sources
    cp Stage${stage}/common.py package/Stage${stage}/sources
    cp dist/client_runner package/Stage${stage}/bin
    cp dist/server_runner package/Stage${stage}/bin
done

rm -rf dist/
rm -rf build/