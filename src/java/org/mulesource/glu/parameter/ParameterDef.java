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

import java.util.HashMap;

public abstract class ParameterDef
{
    /*
    public final static String PARAM_STRING   = "string";           implemented
    public final static String PARAM_PASSWORD = "password";         implemented
    public final static String PARAM_BOOL     = "boolean";          implemented
    public final static String PARAM_DATE     = "date";
    public final static String PARAM_TIME     = "time";
    public final static String PARAM_NUMBER   = "number";           implemented
    public final static String PARAM_URI      = "uri";
    */
    
    public String  ptype;
    public String  desc;
    public boolean required;
    
    public ParameterDef(String ptype, String desc, boolean required)
    {
        this.ptype    = ptype;
        this.desc     = desc;
        this.required = required;
    }
    
    public abstract Object getDefaultVal();
    
    public HashMap<String, Object> asDict()
    {
        HashMap<String, Object> d = new HashMap<String, Object>();
        
        d.put("type",     ptype);
        d.put("desc",     desc);
        d.put("required", required);
        d.put("default",  getDefaultVal());
        
        return d;
    }

    public String html_type(String name)   // strange naming? This is called from Python code as well
    {
        return "<input type=text name="+name+" />";
    }

}


