#!/bin/bash
cd ..

git submodule init
git submodule update

cd nzmqt

# Setup project directories.
mkdir -p externals/include

# Copy cppzmq related files.
cp externals-src/cppzmq/zmq.hpp externals/include

