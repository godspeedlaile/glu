/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.clientapi;

import java.util.HashMap;
import java.lang.Number;
import java.math.BigDecimal;

public class GluParameter
{
    protected final static String DESC_KEY     = "desc";
    protected final static String REQUIRED_KEY = "required";
    protected final static String TYPE_KEY     = "type";
    protected final static String DEFAULT_KEY  = "default";

    protected String              name;
    protected String              desc;
    protected boolean             required;
    protected String              typeStr;
    
    public static boolean boolConvert(Object val)
    {
        if (val.getClass() == Boolean.class) {
            return ((Boolean)val).booleanValue();
        }
        
        String valStr = ((String)val).toLowerCase();
        if (valStr.equals("y")  ||  valStr.equals("yes")  ||  valStr.equals("t")  ||
            valStr.equals("true")  ||  valStr.equals("1"))
        {
            return true;
        }
        else {
            return false;
        }
    }
    
    public static Object numstrToNum(Object val) throws GluClientException
    {
        Class cl = val.getClass();
        if (cl == Integer.class  ||  cl == Float.class  ||  cl == Double.class  ||  cl == BigDecimal.class) {
            return val;
        }
        else if (cl == String.class) {
            return new BigDecimal((String)val);
        }
        else {
            throw new GluClientException("Cannot convert number.");
        }
    }
    

    public GluParameter(String name, HashMap<String, ?> pdef)
    {
        this.name = name;
        try {
            desc     = (String)pdef.get(DESC_KEY);
            required = boolConvert(pdef.get(REQUIRED_KEY));
            typeStr  = (String)pdef.get(TYPE_KEY);
        }
        
    }

}


