;Create daily spectra from B1/B2 data.
;((See call_plot_b1_b2_spec.py))


pro plot_b1_b2_spec

  rbsp_efw_init


  args = command_line_args()
  if KEYWORD_SET(args) then begin
      sc = args[0]
      type = args[1]
      date = args[2]

  endif else begin
      sc = 'a'
      type = 'mscb1'
      date = '2014-05-09'

  endelse


  yyyymmdd = time_string(date,format=6)
  yyyymmdd = strmid(yyyymmdd,0,8)
  yyyy = strmid(yyyymmdd,0,4)
  mm = strmid(yyyymmdd,4,2)



  ;Now from IDL load the individual files and get spectra
  lp = '/Users/aaronbreneman/Desktop/code/Aaron/github.umn.edu/rbsp_split_b1_cdf/out/*.cdf'
  files = FILE_SEARCH(lp)


  loadct,39

  for i=0,n_elements(files)-1 do begin
    cdf2tplot,files[i]

    ;get timerange for data
    split_vec,'mscb1'
    get_data,'mscb1_z',data=d
    t0 = time_string(min(d.x,/nan),format=2)
    t1 = time_string(max(d.x,/nan),format=2)


    rbsp_spec,'mscb1_z',npts=2048,n_ave=2
    ylim,'mscb1_z_SPEC',30,6000,1
    zlim,'mscb1_z_SPEC',1d-6,1d2,1
;    tplot,'mscb1_z_SPEC'\
;stop
    fn = 'rbsp'+sc+'_'+type+'_spec_'+t0+'-'+t1
    popen,'~/Desktop/'+fn
    tplot,'mscb1_z_SPEC'
    pclose

    store_data,'*',/delete
  endfor

end
