/*
 * $Id$
 * --------------------------------------------------------------------------------------
 * Copyright (c) MuleSource, Inc.  All rights reserved.  http://www.mulesource.com
 *
 * The software in this package is published under the terms of the CPAL v1.0
 * license, a copy of which has been included with this distribution in the
 * LICENSE.txt file.
 */

package org.mulesource.glu;

import java.util.HashMap;

import org.mulesource.glu.component.api.HttpMethod;
import org.mulesource.glu.component.api.HttpResult;

public interface ResourceAccessorInterface
{
    public HttpResult accessResourceProxy(String uri, String input, HashMap params, HttpMethod method);
}


