#!/bin/bash
# Altered from pythondeps.sh
# The second parameter is %{scl_prefix}, which is used to prefix python(abi).

[ $# -ge 1 ] || {
    cat > /dev/null
    exit 0
}

case $1 in
-P|--provides)
    shift
    # Match buildroot/payload paths of the form
    #    /PATH/OF/BUILDROOT/%{_scl_root}/usr/bin/pythonMAJOR.MINOR
    # generating a line of the form
    #    %{scl_prefix}python(abi) = MAJOR.MINOR
    # (Don't match against -config tools e.g. /usr/bin/python2.6-config)
    if [ "x$1" = "x" ]; then
        grep "/usr/bin/python.\..$" \
            | sed -e "s|.*/usr/bin/python\(.\..\)|python(abi) = \1|"
    else
        grep "/opt/.*/usr/bin/python.\..$" \
            | sed -e "s|.*/usr/bin/python\(.\..\)|$1python(abi) = \1|"
    fi

    if [ "x$1" != "x" ]; then
        grep "pkgconfig(.*$" \
            | sed -e "s|pkgconfig(|$1pkgconfig(|"
    fi
   ;;
-R|--requires)
    shift
    # Match buildroot paths of the form
    #    /PATH/OF/BUILDROOT/%{scl_root}/usr/lib/pythonMAJOR.MINOR/  and
    #    /PATH/OF/BUILDROOT/%{scl_root}/usr/lib64/pythonMAJOR.MINOR/
    # generating (uniqely) lines of the form:
    #    %{scl_prefix}python(abi) = MAJOR.MINOR
    if [ "x$1" = "x" ]; then
        grep "/usr/lib[^/]*/python.\../.*" \
            | sed -e "s|.*/usr/lib[^/]*/python\(.\..\)/.*|python(abi) = \1|g" \
            | sort | uniq
    else
        grep "/opt/.*/usr/lib[^/]*/python.\../.*" \
            | sed -e "s|.*/usr/lib[^/]*/python\(.\..\)/.*|$1python(abi) = \1|g" \
            | sort | uniq
    fi
    ;;
esac

exit 0
