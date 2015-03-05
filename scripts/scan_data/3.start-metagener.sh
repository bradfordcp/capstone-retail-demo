#!/bin/bash

# This syntax is an implicit "daemonize" in bash.
# The intermediate process exits, leaving the inner
# process to be inherited by init. It's not a proper daemon process,
# but close enough

(
    (
        cd /cornerstone/scripts/scan_data;
        export PATH=/usr/lib/jvm/java-8-oracle/bin:$PATH;
        export JAVA_HOME=/usr/lib/jvm/java-8-oracle;
        java -jar metagener-webapi-1.0-SNAPSHOT.jar server retail.yaml
    ) &
) &
