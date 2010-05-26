/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu.component;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Vector;

import org.mulesource.glu.component.api.*;


@ComponentInfo(name        = "JavaTwitterComponent",
               description = "This is a Java implementation of a Twitter component",
               doc         = "The Twitter component is designed to provide access to a Twitter account." +
                             "It can be used to get status as well as update status.")
public class JavaTwitterComponent extends BaseComponent
{    
    @Parameter(name="account_name", desc="Twitter account name")
    public String account_name = null;
    
    @Parameter(name="account_password", desc="Password")
    public String account_password = null;

    private String getStatus()
    {
        HttpResult res = httpGet("http://api.twitter.com/1/users/show.json?screen_name=" + account_name);
        if (res.status == HTTP.OK) {
            return res.data;
        }
        else {
            return "Problem with Twitter: " + res.data;
        }
    }
    
    private String postStatus(String data)
    {
        httpSetCredentials(account_name, account_password);
        HttpResult res = httpPost("http://api.twitter.com/1/statuses/update.xml", "status=" + data);
        return res.data;
    }
    
    @Service(description = "You can GET the status or POST a new status to it.")
    public Result status(String method, String input)
    {
        int    status = HTTP.OK;
        String data;
        /*
        if (method.equals(HTTP.GET_METHOD)) {
            data = getStatus();
        }
        else {
            data = postStatus(input);
        }
        */
        data = "Blah: " + input;
        return new Result(status, data);
    }
}


