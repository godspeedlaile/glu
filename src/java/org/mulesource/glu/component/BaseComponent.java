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

import com.sun.net.httpserver.Headers;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.lang.annotation.Annotation;
import java.lang.reflect.*;
import java.math.BigDecimal;

import org.mulesource.glu.GluHttpRequest;
import org.mulesource.glu.ResourceAccessorInterface;
import org.mulesource.glu.Settings;
import org.mulesource.glu.component.api.*;
import org.mulesource.glu.exception.GluException;
import org.mulesource.glu.parameter.*;

public abstract class BaseComponent
{
    public final String                              LANGUAGE = "JAVA";
    public       ComponentDescriptor                 componentDescriptor = null;
    public       ResourceAccessorInterface           resourceAccessor;

    protected    HashMap<String, Object>             services;

    private      GluHttpRequest                      httpRequest;
    private      String                              resourceName;
    private      BaseComponentCapabilities           baseCapabilities;
    
    private      boolean                             annotationsHaveBeenParsed = false;
    // We use the following to record the order of parameters as well as their
    // Java types for each service when we are parsing the annotations. Later,
    // this helps our service-method calling proxy to arrange the parameters in
    // the right order - since Java does not allow the **fkwargs notation of named
    // parameters - and also allows us to do the necessary type casting.
    private      HashMap<String, ArrayList<String>>  paramOrder;
    private      HashMap<String, ArrayList<Class<?>>>   paramTypes;
    
    public BaseComponent()
    {
        this.resourceName     = null;
        this.httpRequest      = null;
        this.baseCapabilities = null;
    }
    
    public void setBaseCapabilities(BaseComponentCapabilities baseCapabilities)
    {
        this.baseCapabilities = baseCapabilities;
    }
    
    private ComponentDescriptor getComponentDescriptor() throws GluException
    {
        if (componentDescriptor == null) {
            annotationParser();
        }
        return componentDescriptor;
    }
    
    public void setResourceName(String resourceName)
    {
        this.resourceName = resourceName;
    }
    
    public void setRequest(GluHttpRequest request)
    {
        this.httpRequest = request;
    }
    
    public String getDocs()
    {
        return this.componentDescriptor.getDocs();
    }
    
    public String getRequestUri()
    {
        return httpRequest.getRequestURI();
    }
    
    public Headers getRequestHeaders()
    {
        return httpRequest.getRequestHeaders();
    }
    
    public HttpResult accessResource(String uri)
    {
        return accessResource(uri, null, null, HTTP.GET);
    }

    public HttpResult accessResource(String uri, String input)
    {
        return accessResource(uri, input, null, HTTP.GET);
    }

    public HttpResult accessResource(String uri, String input, Map<?,?> params)
    {
        return accessResource(uri, input, params, HTTP.GET);
    }
    
    public HttpResult accessResource(String uri, String input, Map<?,?> params, HttpMethod method)
    {
        return resourceAccessor.accessResourceProxy(uri, input, params, method);
    }
    
    private ParameterDef createParamDefType(Class<?> paramType, String desc,
                                            boolean required, String defaultVal)
    {
        ParameterDef pdef = null;
        if (paramType == String.class) {
            pdef = new ParameterDefString(desc, required, defaultVal);
        }
        else if (paramType == Integer.class ||  paramType == BigDecimal.class  ||
                 paramType == Double.class  ||  paramType == Float.class ||
                 paramType == int.class     ||  paramType == float.class ||
                 paramType == double.class)
        {
            pdef = new ParameterDefNumber(desc, required, new BigDecimal(defaultVal));
        }
        else if (paramType == Boolean.class) {
            pdef = new ParameterDefBoolean(desc, required, new Boolean(defaultVal));
        }
        return pdef;
    }
        
    public void annotationParser() throws GluException
    {
        if (annotationsHaveBeenParsed  ||  componentDescriptor != null) {
            return;
        }
        Class<? extends BaseComponent> myclass = this.getClass();
        
        /*
         * Examine the class annotations to get information about the
         * component.
         */
        ComponentInfo ci = this.getClass().getAnnotation(ComponentInfo.class);
        if (ci == null) {
            throw new GluException("Component does not have a ComponentInfo annotation");
        }
        componentDescriptor = new ComponentDescriptor(ci.name(), ci.description(), ci.doc());
        
        /*
         * Examine field annotations to identify resource creation
         * time parameters.
         */
        for (Field f: myclass.getFields()) {
            Parameter fa = f.getAnnotation(Parameter.class);
            if (fa != null) {
                String  paramName   = fa.name();
                String  paramDesc   = fa.desc();
                String  defaultVal  = null;
                boolean required    = true;
                
                // Check if we have a default value and set that one as well
                Default fad = f.getAnnotation(Default.class);
                if (fad != null) {
                    defaultVal = fad.value();
                    required   = false;
                }
                Class<?> ftype = f.getType();
                componentDescriptor.addParameter(paramName,
                                                 createParamDefType(ftype, paramDesc, required, defaultVal));
            }
        }
        
        /*
         * Examine the method annotations to identify service methods
         * and their parameters.
         */
        paramOrder = new HashMap<String, ArrayList<String>>();
        paramTypes = new HashMap<String, ArrayList<Class<?>>>();
        for (Method m: myclass.getMethods()) {
            if (m.isAnnotationPresent(Service.class)) {
                String            serviceName         = m.getName();
                Service           at                  = m.getAnnotation(Service.class);
                ServiceDescriptor sd                  = new ServiceDescriptor(at.description());
                Class<?>[]        types               = m.getParameterTypes();
                Annotation[][]    allParamAnnotations = m.getParameterAnnotations();
                int i = 0;
                ArrayList<String> positionalParams = new ArrayList<String>();
                for (Annotation[] pa : allParamAnnotations) {
                    String  name       = null;
                    String  desc       = null;
                    boolean required   = true;
                    String  defaultVal = null;
                    for (Annotation a: pa) {
                        if (a.annotationType() == Parameter.class) {
                            name = ((Parameter)a).name();
                            desc = ((Parameter)a).desc();
                            if (!paramOrder.containsKey(serviceName)) {
                                paramOrder.put(serviceName, new ArrayList<String>());
                                paramTypes.put(serviceName, new ArrayList<Class<?>>());
                            }
                            if (((Parameter)a).positional()) {
                                positionalParams.add(name);
                            }
                            paramOrder.get(serviceName).add(name);
                            paramTypes.get(serviceName).add(types[i]);
                        }
                        else if (a.annotationType() == Default.class) {
                            defaultVal = ((Default)a).value();
                            required = false;                            
                        }
                    }
                    if (name != null) {                     
                        sd.addParameter(name, createParamDefType(types[i], desc, required, defaultVal));
                    }
                    ++i;
                }
                if (!positionalParams.isEmpty()) {
                    sd.setPositionalParameters(positionalParams);
                }
                componentDescriptor.addService(m.getName(), sd);
            }
        }
        annotationsHaveBeenParsed = true;
    }
    
    public HashMap<String, ArrayList<String>> getParameterOrder() throws GluException
    {
        annotationParser();

        // Returns the order in which parameters were defined
        return paramOrder;
    }
    
    public HashMap<String, ArrayList<Class<?>>> getParameterTypes() throws GluException
    {
        annotationParser();

        // Returns the order in which parameters were defined
        return paramTypes;
    }
    
    public String getMyResourceName()
    {
        return resourceName;
    }
    
    public String getMyResourceUri()
    {
        return Settings.PREFIX_RESOURCE + "/" + getMyResourceName();
    }
    
    public FileStore getFileStorage()
    {
        return baseCapabilities.getFileStorage();
    }

    public FileStore getFileStorage(String namespace)
    {
        return baseCapabilities.getFileStorage(namespace);
    }
    
    public void httpSetCredentials(String accountName, String password)
    {
        baseCapabilities.httpSetCredentials(accountName, password);
    }
    
    public HttpResult httpGet(String url)
    {
        return baseCapabilities.httpGet(url);
    }
    
    public HttpResult httpGet(String url, HashMap<String, String> headers)
    {
        return baseCapabilities.httpGet(url, headers);
    }
    
    public HttpResult httpPost(String url, String data)
    {
        return baseCapabilities.httpPost(url, data);
    }
    
    public HttpResult httpPost(String url, String data, Map<String, String> headers)
    {
        return baseCapabilities.httpPost(url, data, headers);
    }
    
    private HashMap<String, Object> changeParamsToPlainDict(Map<String, ParameterDef> paramDict)
    {
        HashMap<String, Object> d = new HashMap<String, Object>();
        for (String name: paramDict.keySet()) {
            d.put(name, paramDict.get(name).asDict());
        }
        return d;
    }
    
    public HashMap<String, Object> getMetaData() throws GluException
    {
        annotationParser();

        HashMap<String, Object> d = new HashMap<String, Object>();
        
        d.put("uri",      getCodeUri());
        d.put("name",     getName());
        d.put("desc",     getDesc());
        d.put("doc",      getCodeUri() + "/doc");
        d.put("params",   changeParamsToPlainDict(componentDescriptor.getParamMap()));
        d.put("services", _getServices(null));
        
        HashMap<String, ParameterDef> rp = new HashMap<String, ParameterDef>();
        rp.put("suggested_name", new ParameterDefString("Can be used to suggest the resource name to the server",
                                                        true, ""));
        rp.put("desc",           new ParameterDefString("Specifies a description for this new resource",
                                                        false, "A '" + getName() + "' resource")); 

        d.put("resource_creation_params", changeParamsToPlainDict(rp));
        
        return d;
    }
    
    public String getName() throws GluException
    {
        return getComponentDescriptor().getName();
    }
    
    public String getDesc() throws GluException
    {
        return getComponentDescriptor().getDesc();
    }
    
    public String getDoc() throws GluException
    {
        return getComponentDescriptor().getDocs();
    }
    
    public String getCodeUri()
    {
        String name;
        try {
            name = getName();
        }
        catch (Exception e) {
            name = "";
        }
        return Settings.PREFIX_CODE + "/" + name;
    }
    
    /*
     * Following are some methods that are used by the framework and that are not part
     * of the official component-API.
     */
    
    /*
     * Return a dictionary of all defined services. resourceBaseUri may be set to null,
     * in which case all service URLs are relative to the code URL of the component.
     */
    public HashMap<String, Object> _getServices(String resourceBaseUri) throws GluException
    {
        annotationParser();

        // Get the base URI for all services. If no resource base URI
        // was defined (can happen when we just look at code meta data)
        // then we use the code base URI instead.
        String baseUri;        
        if (resourceBaseUri == null) {
            baseUri = getCodeUri();
        }
        else {
            baseUri = resourceBaseUri;
        }
        
        // Create a map of service descriptions.
        if (componentDescriptor.getServicMap() != null  &&  !componentDescriptor.getServicMap().isEmpty()) {            
            services = componentDescriptor.getServicesAsPlainDict();
            HashMap<String, Object> ret = new HashMap<String, Object>();
            for (String name: services.keySet()) {
                HashMap<String, Object> thisService = (HashMap<String, Object>)services.get(name);
                thisService.put("uri", baseUri + "/" + name);
                ret.put(name, thisService);
                HashMap<String, Object> params = (HashMap<String, Object>)thisService.get("params");
                if (params != null) {
                    for (String pname: params.keySet()) {
                        Object param = params.get(pname);
                        if (param instanceof ParameterDef) {
                            // Need the type check since we may have constructed the
                            // representation from storage, rather than in memory.
                            // If it's from storage then we don't have ParameterDefs
                            // in this dictionary here, so we don't need to convert
                            // anything.
                            param = ((ParameterDef)param).asDict();
                            params.put(pname, param);
                        }
                    }
                }
            }
            
            return ret;
        }
        else {
            // No services defined? Nothing to return...
            return null;
        }
    }
 }


