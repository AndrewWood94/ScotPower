set -e

function pgvector_installed {
    test -f /usr/share/postgresql/14/extension/vector.control
}

if pgvector_installed; then
    echo "pgvector is already installed."
else
    echo "Installing required packages"
    sudo apt update
    sudo apt install postgresql-server-dev-14
    git clone https://github.com/pgvector/pgvector.git
    cd pgvector
    make
    sudo make install
    cd ..
    rm -rf pgvector
fi
