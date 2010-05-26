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

import org.mulesource.glu.component.api.FileStore;
import org.mulesource.glu.component.api.HttpResult;

public abstract class BaseComponentCapabilities
{
    // Storage
    public abstract FileStore  getFileStorage(String namespace);
    public          FileStore  getFileStorage()
    {
        return getFileStorage("");
    }
        
    // HTTP accesses
    public abstract void       httpSetCredentials(String accountName, String password);
    public abstract HttpResult httpGet(String url);
    public abstract HttpResult httpPost(String url, String data);
}


