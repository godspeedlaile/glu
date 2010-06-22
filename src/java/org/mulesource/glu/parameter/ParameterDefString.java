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

public class ParameterDefString extends ParameterDef
{
    private String defaultVal;
    
    public ParameterDefString(String desc)
    {
        this(desc, true, null);
    }
    
    public ParameterDefString(String desc, String defaultVal)
    {
        this(desc, false, defaultVal);
    }
    
    public ParameterDefString(String desc, boolean required, String defaultVal)
    {
        super("string", desc, required);
        this.defaultVal = defaultVal;
    }

    @Override
    public Object getDefaultVal()
    {
        return defaultVal;
    }
}


