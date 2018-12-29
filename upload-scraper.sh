root=`pwd`
build_name="deploy.zip"
deploy_bucket="derp-backup-sync"

function do_setup {
    cd $root/scraper
    if [ ! -d lib ] ; then
        echo "Installing libraries to lib/"
        mkdir lib
        pip install -r requirements.txt -t ./lib/ > "setup.log"
        echo "done. log in setup.log"
    else
        echo "no setup action needed"
    fi
}

function do_clean {
    cd $root/scraper
    echo 'deleting scraper/build'
    rm -rf build
    echo 'done deleting scraper/build'
}

function do_build {
    cd $root/scraper

    if [ ! -d lib ] ; then
        echo "lib doesn't exist. please install your libraries."
    else

        echo "creating build directory"
        mkdir build
        echo "moving files"
        cp *.py build/
        echo "moving libraries"
        cp -r lib/* build/
        cd build
        echo "zipping..."
        zip -r $build_name . > "zip.log"
        echo "done. zip output at 'zip.log'"
    fi
}

function do_upload {
    cd $root/scraper

    if [ -z $build_name ] ; then
        echo "Error, deploy zip not found"
    else
        echo "Starting upload to $deploy_bucket."
        aws s3 cp $build_name s3://$deploy_bucket
        echo "Uploaded $build_name to $deploy_bucket!"
    fi
}

if [ $1 == 'setup' ] ; then
    do_setup

elif [ $1 == 'clean' ] ; then
    do_clean

elif [ $1 == 'build' ] ; then
    do_build

elif [ $1 == 'upload' ] ; then
    do_upload

else
    do_clean
    do_build
    do_upload
fi


# https://s3.amazonaws.com/derp-backup-sync/$build_name
#aws lambda update-function-code --function-name scraper-hn-inlet --s3-bucket derp-backup-sync --s3-key $build_name --publish
