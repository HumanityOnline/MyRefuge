sudo -u postgres -i <<'EOF'
exists=`psql --list | egrep '\btemplate_postgis\b'`
# Check if the template_postgis database exists. If not, create it.
if [ -z "$exists" ]; then
  # Creating the template spatial database.
  createdb -E UTF8 template_postgis
  psql -d template_postgis -c "CREATE EXTENSION postgis;"
fi

USER=myrefuge
createuser -P -D -R -S $USER
createdb -T template_postgis -E 'utf8' -O $USER myrefuge

EOF
