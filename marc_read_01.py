import datetime, glob, logging, os, pprint
from pymarc import MARCReader  # <https://gitlab.com/pymarc/pymarc>

## set up basic loggging to console ---------------------------------
logging.basicConfig(
    # filename=settings['LOG_PATH'],
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    )
log = logging.getLogger(__name__)
log.debug( 'logging ready' )


FILES_DIR = './source_files'


def process_marc_files():

    first_start_time = datetime.datetime.now()

    ## get list of files
    marc_file_list: list = create_marc_file_list()

    ## for each file...
    records_processed = 0
    for marc_path in marc_file_list:

        file_start_time = datetime.datetime.now()
        log.debug( 'new file...' )
        log.debug( f'marc_file_path, ``{marc_path}``' )

        with open( marc_path, 'rb' ) as fh:
            reader = MARCReader( fh )
            for record in reader:
                records_processed += 1

                if record is None:
                    log.warning('record is None; continuing')
                    continue

                log.debug( 'new record...' )
                log.debug( f'type(record), ``{type(record)}``' )
                log.debug( f'record, ``{record}``' )

                if record.get_fields('245'):
                    full_title = record['245']['a']
                    log.debug( f'full_title, ``{full_title}``'  )

                bib = record['907']['a']
                log.debug( f'bib_url, ``https://search.library.brown.edu/catalog/{bib}``' )

                # break

        file_end_time = datetime.datetime.now()
        log.debug( f'file-elapsed-time, ``{file_end_time - file_start_time}``' )

    all_files_end_time = datetime.datetime.now()
    elapsed_time = all_files_end_time - first_start_time
    log.debug( f'all-files-elapsed-time, ``{elapsed_time}``' )
    log.debug( f'records_processed, ``{records_processed}``' )

    ## calculate records-processed-per-second
    seconds = elapsed_time.total_seconds()
    records_per_second = int( records_processed / seconds )
    log.debug( f'records_per_second, ``{records_per_second}``' )


    ## end process_marc_files()


def create_marc_file_list():
    marc_file_list = sorted( glob.glob('%s/*.mrc' % FILES_DIR) )
    print( f'marc_file_list, ``{pprint.pformat(marc_file_list)}``' )
    return marc_file_list


if __name__ == '__main__':
    log.debug( 'starting `main`' )
    process_marc_files()
    log.debug( '`main` complete' )
