/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.parameter;

public class ParameterDefBoolean extends ParameterDef
{
    private boolean defaultVal;
    
    public ParameterDefBoolean(String desc)
    {
        this(desc, true, false);
    }
        
    public ParameterDefBoolean(String desc, boolean defaultVal)
    {
        this(desc, false, defaultVal);
    }
    
    public ParameterDefBoolean(String desc, boolean required, boolean defaultVal)
    {
        super("boolean", desc, required);
        this.defaultVal = defaultVal;
    }

    @Override
    public Object getDefaultVal()
    {
        return defaultVal;
    }

    @Override
    public String html_type(String name)   // strange naming? This is called from Python code as well
    {
        String ret = "<label for=" + name + "_yes><input type=radio id="+name+"_yes name="+name+" value=yes />yes</label><br>";
        return ret + "<label for=" + name + "_no><input type=radio id="+name+"_no name="+name+" value=no />no</label><br>";
    }
}


