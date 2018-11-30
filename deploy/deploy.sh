#!/usr/bin/env bash

mkdir pkg
pip install -r requirements.txt --target pkg

cp -R svc pkg

chmod -R 755 pkg/

cd pkg
zip -r ../lambda_pkg.zip .

rm -rf pkg

aws lambda update-function-code --function-name $LAMBDA_FUNCTION --zip-file fileb://lambda_pkg.zip
