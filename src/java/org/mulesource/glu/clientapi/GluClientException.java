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

/**
 * The base class for all exceptions that are thrown by
 * the Glu client API.
 */
public class GluClientException extends Exception
{
    /**
     * Construct a new exception.
     * 
     * @param message   The human readable message for this exception.
     */
    public GluClientException(String message)
    {
        super(message);
    }
}


